from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import datetime
from pathlib import Path

app = FastAPI(
    title="Borsa API",
    description="Jenkins ve Docker ile ayağa kaldırılmış güvenli borsa sistemi",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_dist_path = Path(__file__).parent / "frontend" / "dist"
frontend_assets_path = frontend_dist_path / "assets"
if frontend_dist_path.exists():
    if frontend_assets_path.exists():
        app.mount("/assets", StaticFiles(directory=frontend_assets_path), name="frontend-assets")
    app.mount("/frontend", StaticFiles(directory=frontend_dist_path), name="frontend")

# --- Veri Modelleri ---
class Haber(BaseModel):
    id: int
    baslik: str
    icerik: str
    kaynak: str
    tarih: str

# --- Mevcut Endpointler ---
@app.get("/")
def read_root():
    return {"mesaj": "Borsa API sistemine hoş geldiniz, sistem aktif."}

@app.get("/health")
def health_check():
    return {"durum": "sağlıklı", "servis": "çalışıyor"}

# --- Yeni: Haberler Endpointi ---
@app.get("/haberler", response_model=List[Haber])
async def borsa_haberlerini_getir():
    # TODO: İleride buraya httpx ile gerçek bir borsa haber API'si bağlantısı yapılacak.
    # Şimdilik localhost'ta sistemi test etmek için sahte (mock) veriler dönüyoruz.
    ornek_haberler = [
        Haber(
            id=1,
            baslik="Merkez Bankası Faiz Kararını Açıkladı",
            icerik="Merkez Bankası politika faizini piyasa beklentileri doğrultusunda sabit bıraktı.",
            kaynak="Ekonomi Gündemi",
            tarih=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        ),
        Haber(
            id=2,
            baslik="Teknoloji Hisselerinde Büyük Dalgalanma",
            icerik="Küresel piyasalardaki belirsizlik sebebiyle teknoloji şirketlerinin hisseleri güne dalgalı başladı.",
            kaynak="Finans Portalı",
            tarih=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        )
    ]
    return ornek_haberler


@app.get("/uygulama")
def frontend_uygulama():
    index_file = frontend_dist_path / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "mesaj": "Frontend build dosyası bulunamadı. Önce frontend build alın.",
        "yol": str(index_file)
    }