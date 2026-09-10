import pandas as pd
from sqlalchemy.orm import Session
from app.models import ProductionData
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AgroETL")

class AgroETL:
    def __init__(self, db_session: Session):
        self.db = db_session

    def extract(self, file_path: str) -> pd.DataFrame:
        logger.info(f"Iniciando extração do arquivo: {file_path}")
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Extração concluída com sucesso. Linhas lidas: {len(df)}")
            return df
        except Exception as e:
            logger.error(f"Erro ao ler arquivo: {str(e)}")
            raise e

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Iniciando transformação e validação de qualidade de dados...")
        
        df.columns = df.columns.str.strip().str.lower()
        
        initial_count = len(df)
        df = df.drop_duplicates(subset=["farm_id", "crop_type", "harvest_date"])
        logger.info(f"Duplicatas removidas: {initial_count - len(df)}")

        df["harvest_date"] = pd.to_datetime(df["harvest_date"], errors="coerce")
        df["area_hectares"] = pd.to_numeric(df["area_hectares"], errors="coerce")
        df["yield_tons"] = pd.to_numeric(df["yield_tons"], errors="coerce")
        df["crop_type"] = df["crop_type"].str.strip().str.capitalize()
        df["region"] = df["region"].str.strip().str.upper()

        df = df.dropna(subset=["farm_id", "crop_type", "harvest_date", "area_hectares", "yield_tons"])
        df = df[(df["area_hectares"] > 0) & (df["yield_tons"] >= 0)]

        df["productivity_tons_per_ha"] = (df["yield_tons"] / df["area_hectares"]).round(2)
        df["harvest_date"] = df["harvest_date"].dt.date

        logger.info(f"Transformação concluída. Linhas válidas restantes: {len(df)}")
        return df

    def load(self, df: pd.DataFrame) -> int:
        logger.info("Iniciando carga no PostgreSQL...")
        records = df.to_dict(orient="records")
        objects = [ProductionData(**record) for record in records]
        
        try:
            self.db.bulk_save_objects(objects)
            self.db.commit()
            logger.info(f"Carga concluída com sucesso. Registros inseridos: {len(objects)}")
            return len(objects)
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro durante a carga no banco: {str(e)}")
            raise e

    def run_pipeline(self, file_path: str) -> int:
        df_raw = self.extract(file_path)
        df_clean = self.transform(df_raw)
        inserted_rows = self.load(df_clean)
        return inserted_rows
