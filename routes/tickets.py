from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from models.events import Event
from models.ticket import Ticket

router = APIRouter()


class TicketRequest(BaseModel):
    event_id: PydanticObjectId
    user_name: str


@router.post("/buy", status_code=status.HTTP_201_CREATED)
async def buy_ticket(request: TicketRequest):
    """
    Transaction kullanarak güvenli bilet alımı.
    Hem bilet oluşturur hem de stoktan düşer.
    """

    # DÜZELTME BURADA:
    # Event modelinin bağlı olduğu koleksiyon üzerinden Client'a ulaşıyoruz.
    client = Event.get_pymongo_collection().database.client

    # Transaction Başlatma
    # 'async with' bloğu transaction bitince otomatik commit eder.
    # Hata olursa otomatik rollback (geri alma) yapar.
    async with await client.start_session() as session:
        async with session.start_transaction():

            # 1. Etkinliği Getir (Session ile - Kilitli okuma gibi düşün)
            event = await Event.get(request.event_id, session=session)

            if not event:
                raise HTTPException(status_code=404, detail="Etkinlik bulunamadı")

            # 2. Stok Kontrolü
            # Not: Eski kayıtlarında capacity alanı olmayabilir,
            # modelde default=100 vermiştik, Beanie bunu halleder.
            if event.sold_count >= event.capacity:
                raise HTTPException(status_code=400, detail="Biletler tükendi!")

            # 3. Bileti Oluştur
            ticket = Ticket(
                event_id=event.id, user_name=request.user_name, price_paid=event.price
            )
            # Bileti kaydet (Session ile)
            await ticket.create(session=session)

            # 4. Etkinlik Sayaç Güncelleme
            event.sold_count += 1

            # Etkinliği kaydet (Session ile)
            await event.save(session=session)

            return {"message": "Bilet başarıyla alındı", "ticket_id": str(ticket.id)}
