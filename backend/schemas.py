from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, Literal
from datetime import datetime

class ProcessRequest(BaseModel):
    """User request to process a dataset"""
    
    dataset_url: HttpUrl = Field(
        ..., 
        description="URL to ZIP file containing images (S3, Google Drive, Dropbox, etc.)"
    )
    
    instructions: str = Field(
        ...,
        description="Natural language description of desired processing",
        min_length=10,
        max_length=2000,
        examples=[
            "Create 10,000 augmented variations with rotations, flips, and brightness changes",
            "Generate before/after pairs for change detection, with 5000 output samples",
            "Expand this dataset 10x for a Kaggle competition, preserving class distribution",
            "Create spot-the-difference pairs with difficulty levels from easy to hard"
        ]
    )
    
    output_format: Literal["huggingface", "coco", "yolo", "csv", "json"] = Field(
        default="json",
        description="Desired output format"
    )
    
    output_count: Optional[int] = Field(
        default=None,
        description="Desired number of output samples (if not specified in instructions)"
    )

class JobResponse(BaseModel):
    """Response after creating a job"""
    
    job_id: str
    status: Literal["pending", "processing", "completed", "failed"]
    message: str
    estimated_time_minutes: int
    estimated_cost: float

class JobStatus(BaseModel):
    """Current job status"""
    
    job_id: str
    status: Literal["pending", "processing", "completed", "failed", "cancelled"]
    progress: int  # 0-100
    
    # Input info
    input_images_count: int
    instructions: str
    
    # Output info (when completed)
    samples_generated: Optional[int] = None
    download_url: Optional[str] = None
    expires_at: Optional[datetime] = None
    
    # Processing info
    processing_time_seconds: Optional[int] = None
    cost: Optional[float] = None
    
    # Error info (if failed)
    error_message: Optional[str] = None
    
    # Timestamps
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
