from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List
import datetime
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError
import json

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


class KurVerisi(BaseModel):
    usd_try: float
    altin_try_ons: float
    bitcoin_try: float
    tl_karsiligi_usd: float
    tl_karsiligi_altin_ons: float
    tl_karsiligi_bitcoin: float
    guncellenme_zamani: str
    kaynak: str
    guncel_mi: bool

# --- Mevcut Endpointler ---
@app.get("/")
def read_root():
    index_file = frontend_dist_path / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"mesaj": "Borsa API sistemine hoş geldiniz, sistem aktif."}


@app.get("/api")
def api_root():
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


@app.get("/kurlar/anlik", response_model=KurVerisi)
def anlik_kurlar_getir():
    simdi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        with urlopen("https://open.er-api.com/v6/latest/USD", timeout=10) as response:
            usd_data = json.loads(response.read().decode("utf-8"))
        usd_try = float(usd_data["rates"]["TRY"])

        with urlopen("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=try", timeout=10) as response:
            btc_data = json.loads(response.read().decode("utf-8"))
        bitcoin_try = float(btc_data["bitcoin"]["try"])

        with urlopen("https://api.metals.live/v1/spot/gold", timeout=10) as response:
            gold_data = json.loads(response.read().decode("utf-8"))
        altin_usd_ons = float(gold_data[0]["gold"])
        altin_try_ons = altin_usd_ons * usd_try

        return KurVerisi(
            usd_try=round(usd_try, 4),
            altin_try_ons=round(altin_try_ons, 2),
            bitcoin_try=round(bitcoin_try, 2),
            tl_karsiligi_usd=round(1 / usd_try, 6),
            tl_karsiligi_altin_ons=round(1 / altin_try_ons, 8),
            tl_karsiligi_bitcoin=round(1 / bitcoin_try, 10),
            guncellenme_zamani=simdi,
            kaynak="open.er-api.com + coingecko + metals.live",
            guncel_mi=True,
        )
    except (URLError, KeyError, ValueError, IndexError, TimeoutError, json.JSONDecodeError):
        return KurVerisi(
            usd_try=36.2,
            altin_try_ons=73150.0,
            bitcoin_try=3075000.0,
            tl_karsiligi_usd=0.027624,
            tl_karsiligi_altin_ons=0.00001367,
            tl_karsiligi_bitcoin=0.0000003252,
            guncellenme_zamani=simdi,
            kaynak="mock-fallback",
            guncel_mi=False,
        )


@app.get("/uygulama")
def frontend_uygulama():
    index_file = frontend_dist_path / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {
        "mesaj": "Frontend build dosyası bulunamadı. Önce frontend build alın.",
        "yol": str(index_file)
    }