

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uuid

from app.schemas import ProcessRequest, JobResponse, JobStatus
from app.models import Job, JobStatus as JobStatusEnum, User
from app.services.downloader import download_and_extract
from app.services.instruction_parser import InstructionParser
from app.workers.tasks import process_dataset_task
from app.dependencies import get_db, get_current_user, check_usage_limits

app = FastAPI(
    title="Dataset Factory API",
    description="CPU-first image dataset generation with natural language instructions",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# MAIN ENDPOINT: Submit Dataset Processing Request
# ============================================================================

@app.post("/api/v1/process", response_model=JobResponse)
async def create_processing_job(
    request: ProcessRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a dataset processing job
    
    **Example Request:**
```json
    {
        "dataset_url": "https://storage.example.com/my-dataset.zip",
        "instructions": "Create 10,000 augmented images with rotations between -30 and 30 degrees, random flips, and brightness adjustments. Filter out any blurry images.",
        "output_format": "huggingface",
        "output_count": 10000
    }
```
    """
    
    # 1. Parse instructions to extract processing intent
    parser = InstructionParser()
    parsed = parser.parse(request.instructions, request.output_count)
    
    # Extract estimated output count
    estimated_output = parsed.get("estimated_output_count", 1000)
    
    # 2. Check if user has enough quota
    await check_usage_limits(current_user, estimated_output, db)
    
    # 3. Validate URL accessibility (HEAD request)
    try:
        import httpx
        async with httpx.AsyncClient() as client:
            response = await client.head(str(request.dataset_url), timeout=10.0)
            if response.status_code >= 400:
                raise HTTPException(
                    status_code=400,
                    detail=f"Cannot access dataset URL (HTTP {response.status_code})"
                )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid or inaccessible URL: {str(e)}"
        )
    
    # 4. Create job record
    job_id = str(uuid.uuid4())
    
    job = Job(
        id=job_id,
        user_id=current_user.id,
        dataset_url=str(request.dataset_url),
        instructions=request.instructions,
        output_format=request.output_format,
        parsed_operations=parsed,
        status=JobStatusEnum.PENDING,
        estimated_output_count=estimated_output
    )
    
    db.add(job)
    db.commit()
    db.refresh(job)
    
    # 5. Queue Celery task
    task = process_dataset_task.delay(job_id)
    job.celery_task_id = task.id
    db.commit()
    
    # 6. Estimate processing time and cost
    # Rough estimate: 100 images/second on 4 CPU cores
    estimated_time_minutes = max(1, estimated_output // (100 * 60))
    estimated_cost = estimated_output * 0.005  # $0.005 per sample
    
    return JobResponse(
        job_id=job_id,
        status="pending",
        message="Job created successfully. Processing will begin shortly.",
        estimated_time_minutes=estimated_time_minutes,
        estimated_cost=estimated_cost
    )

# ============================================================================
# ENDPOINT: Get Job Status
# ============================================================================

@app.get("/api/v1/jobs/{job_id}/status", response_model=JobStatus)
async def get_job_status(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current status of a processing job
    
    Poll this endpoint every 5 seconds to track progress
    """
    
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user.id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatus(
        job_id=job.id,
        status=job.status.value,
        progress=job.progress,
        input_images_count=job.input_images_count or 0,
        instructions=job.instructions,
        samples_generated=job.samples_generated,
        download_url=job.download_url,
        expires_at=job.expires_at,
        processing_time_seconds=job.processing_time_seconds,
        cost=job.cost,
        error_message=job.error_message,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at
    )

# ============================================================================
# ENDPOINT: Cancel Job
# ============================================================================

@app.post("/api/v1/jobs/{job_id}/cancel")
async def cancel_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Cancel a running job"""
    
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user.id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status not in [JobStatusEnum.PENDING, JobStatusEnum.PROCESSING]:
        raise HTTPException(status_code=400, detail="Job cannot be cancelled")
    
    # Revoke Celery task
    from app.workers.celery_app import celery_app
    celery_app.control.revoke(job.celery_task_id, terminate=True)
    
    job.status = JobStatusEnum.CANCELLED
    db.commit()
    
    return {"message": "Job cancelled successfully"}

# ============================================================================
# ENDPOINT: Download Dataset
# ============================================================================

@app.get("/api/v1/jobs/{job_id}/download")
async def download_dataset(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get download URL for completed dataset
    
    Returns a pre-signed S3 URL that expires in 7 days
    """
    
    job = db.query(Job).filter(
        Job.id == job_id,
        Job.user_id == current_user.id
    ).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.status != JobStatusEnum.COMPLETED:
        raise HTTPException(
            status_code=400,
            detail=f"Job is not completed (status: {job.status.value})"
        )
    
    if not job.download_url:
        raise HTTPException(status_code=500, detail="Download URL not available")
    
    return {
        "download_url": job.download_url,
        "expires_at": job.expires_at,
        "format": job.output_format,
        "sample_count": job.samples_generated,
        "size_mb": job.output_size_mb
    }

# ============================================================================
# Health Check
# ============================================================================

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "2.0.0"
    }
