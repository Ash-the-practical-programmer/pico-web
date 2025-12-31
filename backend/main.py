import uuid
import time
from datetime import datetime
from typing import List, Optional, Literal
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl, Field

# ==========================================
# 1. MODELS (Schemas) - Defined Inline
# ==========================================

class ProcessRequest(BaseModel):
    dataset_url: HttpUrl
    instructions: str = Field(..., min_length=10)
    output_format: Literal["huggingface", "coco", "yolo", "csv", "json"] = "json"
    output_count: Optional[int] = 1000

class JobResponse(BaseModel):
    job_id: str
    status: str
    message: str
    estimated_time_minutes: int

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: int
    download_url: Optional[str] = None
    error_message: Optional[str] = None

# ==========================================
# 2. FAKE DATABASE (In-Memory Dictionary)
# ==========================================
# In a real app, this would be PostgreSQL. 
# For now, we store jobs in RAM. They disappear if the server restarts.
JOBS_DB = {}

# ==========================================
# 3. BACKGROUND WORKER (Replaces Celery)
# ==========================================
def process_dataset_task(job_id: str, url: str, instructions: str):
    """
    Simulates the Heavy AI Processing Logic
    """
    try:
        # Step 1: Update Status to Processing
        JOBS_DB[job_id]["status"] = "processing"
        JOBS_DB[job_id]["progress"] = 10
        print(f"[{job_id}] Starting download from {url}...")
        
        # SIMULATION: Pretend we are downloading/processing
        time.sleep(5) 
        JOBS_DB[job_id]["progress"] = 50
        print(f"[{job_id}] Applying instructions: {instructions}")
        
        time.sleep(5)
        JOBS_DB[job_id]["progress"] = 90
        print(f"[{job_id}] Zipping results...")
        
        # Step 2: Complete
        JOBS_DB[job_id]["status"] = "completed"
        JOBS_DB[job_id]["progress"] = 100
        JOBS_DB[job_id]["download_url"] = f"https://pico-storage.s3.amazonaws.com/{job_id}.zip"
        print(f"[{job_id}] Finished!")

    except Exception as e:
        JOBS_DB[job_id]["status"] = "failed"
        JOBS_DB[job_id]["error_message"] = str(e)

# ==========================================
# 4. MAIN APP
# ==========================================
app = FastAPI(title="Pico Dataset Factory", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow your Next.js app to call this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Pico Factory Online", "active_jobs": len(JOBS_DB)}

@app.post("/api/v1/process", response_model=JobResponse)
async def create_processing_job(request: ProcessRequest, background_tasks: BackgroundTasks):
    # 1. Create Job ID
    job_id = str(uuid.uuid4())
    
    # 2. Store in "Database"
    JOBS_DB[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "progress": 0,
        "created_at": datetime.now(),
        "instructions": request.instructions
    }
    
    # 3. Start Background Task (This runs AFTER response is sent)
    background_tasks.add_task(
        process_dataset_task, 
        job_id, 
        str(request.dataset_url), 
        request.instructions
    )
    
    return JobResponse(
        job_id=job_id,
        status="pending",
        message="Job started",
        estimated_time_minutes=5
    )

@app.get("/api/v1/jobs/{job_id}/status", response_model=JobStatus)
async def get_job_status(job_id: str):
    job = JOBS_DB.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    return JobStatus(
        job_id=job["job_id"],
        status=job["status"],
        progress=job["progress"],
        download_url=job.get("download_url"),
        error_message=job.get("error_message")
    )
