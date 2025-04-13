from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class StatsCreate(BaseModel):
    x: float
    y: float
    z: float


class Stats(StatsCreate):
    id: int
    device_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class TimeRange(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class StatsAnalysis(BaseModel):
    min_value: float
    max_value: float
    count: int
    sum: float
    median: float


class CompleteStatsAnalysis(BaseModel):
    x: StatsAnalysis
    y: StatsAnalysis
    z: StatsAnalysis
    period_start: Optional[datetime] = None
    period_end: Optional[datetime] = None


class DeviceStatsAnalysis(BaseModel):
    device_id: str
    stats: CompleteStatsAnalysis


class UserStatsAnalysis(BaseModel):
    user_id: int
    aggregate_stats: CompleteStatsAnalysis
    device_stats: List[DeviceStatsAnalysis]
