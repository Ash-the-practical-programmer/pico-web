from celery import Celery
from datetime import datetime, timedelta
import tempfile
import shutil
from pathlib import Path

from app.services.downloader import download_and_extract
from app.services.processor import DatasetProcessor
from app.services.exporter import DatasetExporter
from app.models import Job, JobStatus as JobStatusEnum
from app.database import SessionLocal

celery_app = Celery('dataset_factory', broker='redis://localhost:6379/0')

@celery_app.task(bind=True)
def process_dataset_task(self, job_id: str):
    """
    Background task to process dataset
    
    Steps:
    1. Download & extract ZIP
    2. Load images
    3. Apply processing pipeline
    4. Export to desired format
    5. Upload to S3
    6. Update job status
    """
    
    db = SessionLocal()
    temp_dir = None
    
    try:
        # Get job
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return {"error": "Job not found"}
        
        # Update status
        job.status = JobStatusEnum.PROCESSING
        job.started_at = datetime.utcnow()
        job.progress = 0
        db.commit()
        
        # Step 1: Download & Extract (10% progress)
        temp_dir = tempfile.mkdtemp()
        image_dir = download_and_extract(job.dataset_url, temp_dir)
        
        job.progress = 10
        db.commit()
        
        # Count input images
        image_files = list(Path(image_dir).glob("**/*.jpg")) + \
                     list(Path(image_dir).glob("**/*.png")) + \
                     list(Path(image_dir).glob("**/*.jpeg"))
        
        job.input_images_count = len(image_files)
        db.commit()
        
        if len(image_files) == 0:
            raise ValueError("No images found in ZIP file")
        
        # Step 2: Initialize Processor (20% progress)
        processor = DatasetProcessor(
            operations=job.parsed_operations["operations"],
            parameters=job.parsed_operations["parameters"],
            output_count=job.estimated_output_count
        )
        
        job.progress = 20
        db.commit()
        
        # Step 3: Process Images (20% -> 80% progress)
        output_dir = Path(temp_dir) / "output"
        output_dir.mkdir(exist_ok=True)
        
        def progress_callback(current, total):
            progress = 20 + int((current / total) * 60)
            job.progress = progress
            db.commit()
        
        results = processor.process(
            image_files,
            str(output_dir),
            progress_callback=progress_callback
        )
        
        job.samples_generated = results["sample_count"]
        job.progress = 80
        db.commit()
        
        # Step 4: Export to Format (80% -> 90% progress)
        exporter = DatasetExporter()
        export_path = exporter.export(
            results,
            str(output_dir),
            job.output_format
        )
        
        job.progress = 90
        db.commit()
        
        # Step 5: Upload to S3 (90% -> 95% progress)
        from app.services.storage import upload_to_s3, generate_presigned_url
        
        s3_key = f"outputs/{job.user_id}/{job.id}.zip"
        upload_to_s3(export_path, s3_key)
        
        job.progress = 95
        db.commit()
        
        # Step 6: Generate download URL (95% -> 100% progress)
        download_url = generate_presigned_url(
            s3_key,
            expires_in=7 * 24 * 60 * 60  # 7 days
        )
        
        job.download_url = download_url
        job.expires_at = datetime.utcnow() + timedelta(days=7)
        job.output_size_mb = Path(export_path).stat().st_size / (1024 * 1024)
        
        # Complete
        job.status = JobStatusEnum.COMPLETED
        job.completed_at = datetime.utcnow()
        job.progress = 100
        job.processing_time_seconds = (job.completed_at - job.started_at).seconds
        
        # Calculate cost
        job.cost = job.samples_generated * 0.005
        
        # Update user usage
        job.user.samples_used_this_month += job.samples_generated
        
        db.commit()
        
        return {
            "status": "completed",
            "samples_generated": job.samples_generated,
            "download_url": download_url
        }
    
    except Exception as e:
        # Handle errors
        job.status = JobStatusEnum.FAILED
        job.error_message = str(e)
        job.completed_at = datetime.utcnow()
        db.commit()
        
        return {"error": str(e)}
    
    finally:
        # Cleanup
        if temp_dir and Path(temp_dir).exists():
            shutil.rmtree(temp_dir)
        
        db.close()
