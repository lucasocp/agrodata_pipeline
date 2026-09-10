from fastapi import FastAPI, Depends, HTTPException, Query, Status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import os

from app.database import Base, engine, get_db
from app.models import ProductionData
from app.schemas import ProductionDataResponse, KPIResponse
from app.etl import AgroETL

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgroData Pipeline API",
    version="1.0.0",
    description="API REST para consumo de dados agrícolas transformados via pipeline ETL."
)

@app.post("/api/v1/etl/run", status_code=Status.HTTP_200_OK, tags=["ETL"])
def trigger_etl(
    file_path: str = "data/raw_agro_data.csv", 
    db: Session = Depends(get_db)
):
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404, 
            detail=f"Arquivo de dados '{file_path}' não encontrado."
        )
    
    etl_service = AgroETL(db)
    records_processed = etl_service.run_pipeline(file_path)
    
    return {
        "status": "Success",
        "message": "Pipeline ETL executado com sucesso.",
        "records_processed": records_processed
    }

@app.get("/api/v1/production", response_model=List[ProductionDataResponse], tags=["Analytics"])
def list_production_data(
    crop_type: Optional[str] = Query(None, description="Filtrar por tipo de cultura"),
    region: Optional[str] = Query(None, description="Filtrar por região"),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(ProductionData)
    
    if crop_type:
        query = query.filter(ProductionData.crop_type == crop_type.capitalize())
    if region:
        query = query.filter(ProductionData.region == region.upper())

    return query.offset(offset).limit(limit).all()

@app.get("/api/v1/production/kpis", response_model=KPIResponse, tags=["Analytics"])
def get_production_kpis(
    crop_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(
        func.sum(ProductionData.area_hectares).label("total_area"),
        func.sum(ProductionData.yield_tons).label("total_yield"),
        func.avg(ProductionData.productivity_tons_per_ha).label("avg_productivity"),
        func.count(ProductionData.id).label("total_records")
    )
    
    if crop_type:
        query = query.filter(ProductionData.crop_type == crop_type.capitalize())

    result = query.first()

    if not result or result.total_records == 0:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado para os filtros aplicados.")

    return {
        "total_area_hectares": round(result.total_area or 0.0, 2),
        "total_yield_tons": round(result.total_yield or 0.0, 2),
        "average_productivity": round(result.avg_productivity or 0.0, 2),
        "total_records": result.total_records
    }
