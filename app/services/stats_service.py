from datetime import datetime
from typing import List, Optional, Tuple, Dict
from sqlalchemy import func
from sqlalchemy.orm import Session
import statistics

from app.models.stats import Stats
from app.models.device import Device
from app.schemas.stats import StatsCreate, CompleteStatsAnalysis, StatsAnalysis, DeviceStatsAnalysis, UserStatsAnalysis
from app.services.device_service import DeviceService


class StatsService:
    @staticmethod
    def create_device_stats(db: Session, device_id: str, stats_data: StatsCreate) -> Optional[Stats]:
        device = DeviceService.get_device_by_device_id(db, device_id)
        if not device:
            return None

        db_stats = Stats(
            device_id=device.id,
            x=stats_data.x,
            y=stats_data.y,
            z=stats_data.z,
            timestamp=datetime.utcnow()
        )
        db.add(db_stats)
        db.commit()
        db.refresh(db_stats)
        return db_stats

    @staticmethod
    def get_device_stats(
            db: Session,
            device_id: str,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[Stats]:
        device = DeviceService.get_device_by_device_id(db, device_id)
        if not device:
            return []

        query = db.query(Stats).filter(Stats.device_id == device.id)

        if start_time:
            query = query.filter(Stats.timestamp >= start_time)
        if end_time:
            query = query.filter(Stats.timestamp <= end_time)

        return query.order_by(Stats.timestamp.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def analyze_device_stats(
            db: Session,
            device_id: str,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None
    ) -> Optional[CompleteStatsAnalysis]:
        device = DeviceService.get_device_by_device_id(db, device_id)
        if not device:
            return None

        query = db.query(Stats).filter(Stats.device_id == device.id)
        if start_time:
            query = query.filter(Stats.timestamp >= start_time)
        if end_time:
            query = query.filter(Stats.timestamp <= end_time)

        stats = query.all()
        if not stats:
            return None

        x_values = [stat.x for stat in stats]
        y_values = [stat.y for stat in stats]
        z_values = [stat.z for stat in stats]

        x_analysis = StatsService._calculate_stats_analysis(x_values)
        y_analysis = StatsService._calculate_stats_analysis(y_values)
        z_analysis = StatsService._calculate_stats_analysis(z_values)

        return CompleteStatsAnalysis(
            x=x_analysis,
            y=y_analysis,
            z=z_analysis,
            period_start=start_time,
            period_end=end_time
        )

    @staticmethod
    def analyze_user_stats(
            db: Session,
            user_id: int,
            start_time: Optional[datetime] = None,
            end_time: Optional[datetime] = None
    ) -> Optional[UserStatsAnalysis]:
        devices = DeviceService.get_devices_by_user_id(db, user_id)
        if not devices:
            return None

        all_x_values = []
        all_y_values = []
        all_z_values = []

        device_analyses = []

        for device in devices:
            query = db.query(Stats).filter(Stats.device_id == device.id)
            if start_time:
                query = query.filter(Stats.timestamp >= start_time)
            if end_time:
                query = query.filter(Stats.timestamp <= end_time)

            device_stats = query.all()
            if not device_stats:
                continue

            device_x_values = [stat.x for stat in device_stats]
            device_y_values = [stat.y for stat in device_stats]
            device_z_values = [stat.z for stat in device_stats]

            all_x_values.extend(device_x_values)
            all_y_values.extend(device_y_values)
            all_z_values.extend(device_z_values)

            device_x_analysis = StatsService._calculate_stats_analysis(device_x_values)
            device_y_analysis = StatsService._calculate_stats_analysis(device_y_values)
            device_z_analysis = StatsService._calculate_stats_analysis(device_z_values)

            device_analysis = DeviceStatsAnalysis(
                device_id=device.device_id,
                stats=CompleteStatsAnalysis(
                    x=device_x_analysis,
                    y=device_y_analysis,
                    z=device_z_analysis,
                    period_start=start_time,
                    period_end=end_time
                )
            )
            device_analyses.append(device_analysis)

        if not all_x_values:
            return None

        aggregate_x_analysis = StatsService._calculate_stats_analysis(all_x_values)
        aggregate_y_analysis = StatsService._calculate_stats_analysis(all_y_values)
        aggregate_z_analysis = StatsService._calculate_stats_analysis(all_z_values)

        return UserStatsAnalysis(
            user_id=user_id,
            aggregate_stats=CompleteStatsAnalysis(
                x=aggregate_x_analysis,
                y=aggregate_y_analysis,
                z=aggregate_z_analysis,
                period_start=start_time,
                period_end=end_time
            ),
            device_stats=device_analyses
        )

    @staticmethod
    def _calculate_stats_analysis(values: List[float]) -> StatsAnalysis:
        if not values:
            return StatsAnalysis(
                min_value=0.0,
                max_value=0.0,
                count=0,
                sum=0.0,
                median=0.0
            )

        return StatsAnalysis(
            min_value=min(values),
            max_value=max(values),
            count=len(values),
            sum=sum(values),
            median=statistics.median(values)
        )