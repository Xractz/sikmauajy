from fastapi import APIRouter, FastAPI

app = FastAPI(title="Sistem Informasi Kampus Mahasiswa UAJY", version="0.1.0", description="API untuk login ke sikma.uajy.ac.id", docs_url="/" ,redoc_url="/redocs")
router = APIRouter()

from app import routes

app.include_router(router)