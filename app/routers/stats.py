from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session

from app.models.database import get_db
from app.schemas.stats import Stats, StatsCreate, TimeRange, CompleteStatsAnalysis, UserStatsAnalysis
from app.services.stats_service import StatsService
from app.services.device_service import DeviceService
from app.services.user_service import UserService

router = APIRouter(prefix="/stats", tags=["statistics"])


@router.post("/devices/{device_id}", response_model=Stats, status_code=201)
def create_device_stats(
        device_id: str = Path(...),
        stats: StatsCreate = None,
        db: Session = Depends(get_db)
):
    db_device = DeviceService.get_device_by_device_id(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    db_stats = StatsService.create_device_stats(db=db, device_id=device_id, stats_data=stats)
    if db_stats is None:
        raise HTTPException(status_code=500, detail="Failed to create stats")

    return db_stats


@router.get("/devices/{device_id}", response_model=List[Stats])
def read_device_stats(
        device_id: str = Path(...),
        start_time: Optional[datetime] = Query(None),
        end_time: Optional[datetime] = Query(None),
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db)
):
    db_device = DeviceService.get_device_by_device_id(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    stats = StatsService.get_device_stats(
        db=db,
        device_id=device_id,
        start_time=start_time,
        end_time=end_time,
        skip=skip,
        limit=limit
    )

    return stats


@router.post("/devices/{device_id}/analyze", response_model=CompleteStatsAnalysis)
def analyze_device_stats(
        device_id: str = Path(..., description="The device ID to analyze stats for"),
        time_range: TimeRange = None,
        db: Session = Depends(get_db)
):
    db_device = DeviceService.get_device_by_device_id(db, device_id=device_id)
    if db_device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    start_time = None
    end_time = None

    if time_range:
        start_time = time_range.start_time
        end_time = time_range.end_time

    analysis = StatsService.analyze_device_stats(
        db=db,
        device_id=device_id,
        start_time=start_time,
        end_time=end_time
    )

    if analysis is None:
        raise HTTPException(status_code=404, detail="No statistics found for the specified period")

    return analysis


@router.post("/users/{user_id}/analyze", response_model=UserStatsAnalysis)
def analyze_user_stats(
        user_id: int = Path(...),
        time_range: TimeRange = None,
        db: Session = Depends(get_db)
):
    db_user = UserService.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    start_time = None
    end_time = None

    if time_range:
        start_time = time_range.start_time
        end_time = time_range.end_time

    analysis = StatsService.analyze_user_stats(
        db=db,
        user_id=user_id,
        start_time=start_time,
        end_time=end_time
    )

    if analysis is None:
        raise HTTPException(status_code=404, detail="No statistics found for the specified period")

    return analysis