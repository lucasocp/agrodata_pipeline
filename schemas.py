from pydantic import BaseModel, ConfigDict
from datetime import date, datetime

class ProductionDataResponse(BaseModel):
    id: int
    farm_id: str
    crop_type: str
    harvest_date: date
    area_hectares: float
    yield_tons: float
    productivity_tons_per_ha: float
    region: str
    processed_at: datetime

    model_config = ConfigDict(from_attributes=True)

class KPIResponse(BaseModel):
    total_area_hectares: float
    total_yield_tons: float
    average_productivity: float
    total_records: int
