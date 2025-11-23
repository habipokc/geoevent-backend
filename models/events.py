from datetime import datetime
from typing import List, Optional

import pymongo
from beanie import Document
from pydantic import BaseModel, Field


# 1. İç İçe Model (Embedded Document)
# Bu model tek başına veritabanında tablo oluşturmaz, Event'in bir parçası olur.
class Location(BaseModel):
    type: str = "Point"  # GeoJSON standardı gereği her zaman "Point" olacak
    coordinates: List[float]  # [Longitude, Latitude] -> DİKKAT: Önce Boylam!


# 2. Ana Model (Document)
# Bu model veritabanında "events" isimli bir collection oluşturur.
class Event(Document):
    title: str = Field(..., max_length=100)  # Zorunlu alan
    description: Optional[str] = None  # İsteğe bağlı alan
    category: str  # Konser, Tiyatro vb.
    date: datetime  # Etkinlik zamanı
    location: Location  # İşte embedding burada !

    # Ekstra bilgiler
    price: float = 0.0
    capacity: int = 100  # Toplam kontenjan
    sold_count: int = 0  # Satılan bilet sayısı
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "events"

        # Karmaşık index ayarları için 'IndexModel' kullanıyoruz.
        indexes = [
            [("location", "2dsphere")],  # Coğrafi index (Basit tanım)
            "category",  # Basit index
            "date",  # Basit index
            # DETAYLI TEXT INDEX TANIMI (TÜRKÇE)
            pymongo.IndexModel(
                [("title", pymongo.TEXT)],  # Hangi alan: title, Tipi: Text
                name="title_text_tr",  # İndeks adı (Atlas'ta böyle görünecek)
                default_language="turkish",  # İŞTE ARADIĞIMIZ AYAR! 🇹🇷
            ),
        ]

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Büyük Python Buluşması",
                "description": "Backend geliştiriciler toplanıyor.",
                "category": "Teknoloji",
                "date": "2024-12-25T20:00:00",
                "price": 150.0,
                "location": {
                    "type": "Point",
                    "coordinates": [28.9784, 41.0082],  # İstanbul (Kabaca)
                },
            }
        }
