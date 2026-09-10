from sqlalchemy import Column, Integer, String, Float, Date, DateTime, func
from app.database import Base

class ProductionData(Base):
    __tablename__ = "agro_production"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    farm_id = Column(String(50), nullable=False, index=True)
    crop_type = Column(String(50), nullable=False, index=True)
    harvest_date = Column(Date, nullable=False)
    area_hectares = Column(Float, nullable=False)
    yield_tons = Column(Float, nullable=False)
    productivity_tons_per_ha = Column(Float, nullable=False)
    region = Column(String(50), nullable=False)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())
