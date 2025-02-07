from pydantic import BaseModel, Field, validator
from typing import List
from enum import Enum
from datetime import datetime


class AnalysisStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class AnomalyType(str, Enum):
    PRICE = "PRICE"
    QUANTITY = "QUANTITY"
    RATING = "RATING"


class AnomalySeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class Statistics(BaseModel):
    mean: float
    median: float
    std: float


class Product(BaseModel):
    id: int
    name: str
    price: float = Field(..., ge=10, le=500)
    quantity: int = Field(..., ge=1, le=50)
    customer_rating: float = Field(..., ge=1.0, le=5.0)


class Anomaly(BaseModel):
    product_id: int
    type: AnomalyType
    value: float
    expected_range: tuple[float, float]
    severity: AnomalySeverity
    message: str


class AnalysisStats(BaseModel):
    price_stats: Statistics
    quantity_stats: Statistics
    rating_stats: Statistics


class AnalysisResults(BaseModel):
    file_id: str
    status: AnalysisStatus
    statistics: AnalysisStats
    anomalies: List[Anomaly]
    metadata: dict
    total_rows: int
    anomaly_count: int
