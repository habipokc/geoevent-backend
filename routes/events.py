from datetime import datetime
from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

from models.events import Event

# Router oluşturuyoruz. Bu, main.py'deki app'in bir parçası olacak.
router = APIRouter()


# 1. TÜM ETKİNLİKLERİ GETİR (READ - List)
@router.get("/", response_model=List[Event])
async def get_all_events():
    # SQL karşılığı: SELECT * FROM events
    events = await Event.find_all().to_list()
    return events


# 2. TEK BİR ETKİNLİK GETİR (READ - Detail)
@router.get("/{id}", response_model=Event)
async def get_event(id: PydanticObjectId):
    # PydanticObjectId: MongoDB'nin o karmaşık ID yapısını yönetir.

    # SQL karşılığı: SELECT * FROM events WHERE id = ...
    event = await Event.get(id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Etkinlik bulunamadı"
        )
    return event


# 3. ETKİNLİK OLUŞTUR (CREATE)
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Event)
async def create_event(event: Event):
    # Veritabanına kaydet
    await event.create()
    return event


# 4. Etkinlik Güncelleme (Update - Patch)
class UpdateEventSchema(BaseModel):
    # Güncelleme yaparken tüm alanları göndermek zorunda değiliz.
    # Bu yüzden hepsi Optional.
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[float] = None
    date: Optional[datetime] = None
    # Location güncellemesi biraz karmaşık olabilir, şimdilik basit tutalım.


@router.patch("/{id}", response_model=Event)
async def update_event(id: PydanticObjectId, update_data: UpdateEventSchema):
    # 1. Önce güncellenecek kaydı bul
    event = await Event.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Güncellenecek Etkinlik Bulunamadı",
        )

    # 2. Kullanıcının gönderdiği veriyi dict'e çevir
    # exclude_unset=True: Sadece kullanıcının gönderdiği alanları al,
    # göndermediklerini (None olanları) dikkate alma.
    update_query = update_data.dict(exclude_unset=True)

    # 3. MongoDB $set operatörü ile güncelle
    # Beanie bunu bizim için şöyle çevirir: {"$set": {title: "Yeni Başlık"}}

    await event.update({"$set": update_query})

    return event


# 5. Etkinlik Sil (delete)
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(id: PydanticObjectId):
    event = await Event.get(id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Silinecek etkinlik bulunamadı",
        )

    await event.delete()
    # 204 No Content döndüğümüzde body boş gider.
    return None


# 6. YAKINIMDAKİ ETKİNLİKLER (GEOSPATIAL QUERY)
@router.get("/nearby/", response_model=List[Event])
async def get_nearby_events(
    lat: float = Query(..., description="Enlem (Latidude)"),
    lon: float = Query(..., description="Boylam (Longitude)"),
    radius_km: float = Query(10.0, description="Arama yarıçapı (KM cinsinden)"),
):
    """
    Verilen koordinat merkezli, belirtilen yarıçap içindeki etkinlikleri getirir.
    """
    # MongoDB Sorgusu: $near operatörü
    # Mantık: "location" alanı, verilen [lon, lat] noktasına yakından uzağa doğru sıralanır.
    # $maxDistance: Metre cinsinden mesafe kısıtlaması.

    events = await Event.find(
        {
            "location": {
                "$near": {
                    "$geometry": {"type": "Point", "coordinates": [lon, lat]},
                    "$maxDistance": radius_km * 1000,
                }
            }
        }
    ).to_list()

    return events


# İSTATİSTİK CEVAP MODELİ
class CategoryStats(BaseModel):
    category: str = Field(
        alias="_id"
    )  # MongoDB gruplamada id olarak kategori ismini döndürür
    total_events: int
    average_price: float


# 7. KATEGORİ İSTATİSTİKLERİ (AGGREGATION)
@router.get("/stats/categories", response_model=List[CategoryStats])
async def get_category_stats():
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "total_events": {"$sum": 1},
                "average_price": {"$avg": "$price"},
            }
        },
        {"$sort": {"total_events": -1}},
    ]

    cursor = Event.get_pymongo_collection().aggregate(pipeline)
    stats = [doc async for doc in cursor]
    return stats
