from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

app = FastAPI()

@app.on_event("startup")
async def start_db():
    # .env'den verileri al
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")

    if not mongo_uri:
        raise ValueError("MONGO_URI .env dosyasında bulunamadı!")

    # Motor Client oluştur (MongoDB bağlantısı)
    client = AsyncIOMotorClient(mongo_uri)
    
    # Beanie'yi başlat (Şimdilik document_models listesi boş)
    # İleride buraya User, Event gibi modellerimizi ekleyeceğiz.
    await init_beanie(database=client[db_name], document_models=[])
    
    print("✅ MongoDB Bağlantısı Başarılı!")

@app.get("/")
async def root():
    return {"message": "GeoEvent API Çalışıyor!", "status": "Connected"}