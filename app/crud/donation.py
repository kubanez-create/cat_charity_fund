# from typing import Optional
# from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):
    pass
    # async def get_reservations_at_the_same_time(
    #         self,
    #         *,
    #         from_reserve: datetime,
    #         to_reserve: datetime,
    #         meetingroom_id: int,
    #         reservation_id: Optional[int] = None,
    #         session: AsyncSession,
    # ) -> list[Reservation]:
    #     # Выносим уже существующий запрос в отдельное выражение.
    #     select_stmt = select(Reservation).where(
    #         Reservation.meetingroom_id == meetingroom_id,
    #         and_(
    #             from_reserve <= Reservation.to_reserve,
    #             to_reserve >= Reservation.from_reserve
    #         )
    #     )
    #     # Если передан id бронирования...
    #     if reservation_id is not None:
    #         # ... то к выражению нужно добавить новое условие.
    #         select_stmt = select_stmt.where(
    #             # id искомых объектов не равны id обновляемого объекта.
    #             Reservation.id != reservation_id
    #         )
    #     # Выполняем запрос.
    #     reservations = await session.execute(select_stmt)
    #     reservations = reservations.scalars().all()
    #     return reservations

    # async def get_future_reservations_for_room(
    #         self,
    #         room_id: int,
    #         session: AsyncSession,
    # ):
    #     reservations = await session.execute(
    #         select(Reservation).where(
    #             Reservation.meetingroom_id == room_id,
    #             Reservation.to_reserve > datetime.now()
    #         )
    #     )
    #     reservations = reservations.scalars().all()
    #     return reservations

    async def get_by_user(
            self, session: AsyncSession, user: User
    ):
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonation(Donation)
