import os

from beanie import init_beanie
from dotenv import load_dotenv
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from models.events import Event
from models.ticket import Ticket
from routes.events import router as event_router
from routes.tickets import router as ticket_router

load_dotenv()

app = FastAPI(
    title="GeoEvent API",
    description="Konum tabanlı etkinlik yönetim sistemi",
    version="1.0.0",
)


@app.on_event("startup")
async def start_db():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")

    if not mongo_uri:
        raise ValueError("MONGO_URI .env dosyasında bulunamadı!")

    client = AsyncIOMotorClient(mongo_uri)

    # Beanie Başlatma
    await init_beanie(database=client[db_name], document_models=[Event, Ticket])
    print("✅ MongoDB Bağlantısı Başarılı!")


# Router'ı sisteme dahil et
# prefix="/events": Tüm bu rotalar http://.../events ile başlayacak
# tags=["Events"]: Swagger dokümantasyonunda "Events" başlığı altında toplayacak
app.include_router(event_router, prefix="/events", tags=["Events"])
app.include_router(ticket_router, prefix="/tickets", tags=["Tickets"])


@app.get("/")
async def root():
    return {"message": "GeoEvent API Çalışıyor!"}
