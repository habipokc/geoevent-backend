from datetime import datetime
from typing import List, Optional

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
    location: Location  # İşte embedding burada!

    # Ekstra bilgiler
    price: float = 0.0
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "events"  # MongoDB'deki collection adı

        # Indexes: Sorgu performansını artırmak için
        # Burası çok önemli. Geo-spatial sorgular için "2dsphere" indeksi şart!
        indexes = [
            [("location", "2dsphere")],  # Konum bazlı arama için
            [("title", "text")],  # Başlıkta kelime aramak için
            "category",  # Kategoriye göre filtrelemek için
            "date",  # Tarihe göre sıralamak için
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
