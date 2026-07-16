from typing import Literal, Optional

from pydantic import BaseModel, Field


EquipmentStatus = Literal["available", "running", "maintenance", "offline"]
JobStatus = Literal["queued", "in_progress", "completed", "cancelled"]
JobPriority = Literal["low", "normal", "high", "urgent"]


class EquipmentCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    type: str = Field(min_length=1, max_length=80)
    location: Optional[str] = Field(default=None, max_length=120)
    status: EquipmentStatus = "available"


class Equipment(EquipmentCreate):
    id: int
    created_at: str
    updated_at: str


class JobCreate(BaseModel):
    equipment_id: Optional[int] = None
    title: str = Field(min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    status: JobStatus = "queued"
    priority: JobPriority = "normal"


class JobUpdate(BaseModel):
    equipment_id: Optional[int] = None
    title: str = Field(min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    status: JobStatus
    priority: JobPriority


class Job(JobCreate):
    id: int
    created_at: str
    updated_at: str
    completed_at: Optional[str] = None
