from datetime import datetime
from typing import Optional

from beanie import Document, PydanticObjectId
from pydantic import Field


class Ticket(Document):
    event_id: PydanticObjectId  # Hangi etkinlik?
    user_name: str  # Kim aldı? (Normalde User ID olur ama şimdilik isim)
    seat_number: Optional[str] = None
    price_paid: float  # Ne kadara aldı? (Fiyat değişebilir, o anki fiyatı tutmalıyız)
    purchase_date: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = "tickets"
