from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationsDB
from app.services.investment import invest

router = APIRouter()


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    reservation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(reservation, session, user)
    new_donation = await invest(don_obj=new_donation, session=session)
    return new_donation


@router.get(
    "/",
    response_model=list[DonationsDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    donations = await donation_crud.get_multi(session)
    return donations


@router.get(
    "/my",
    response_model=list[DonationDB],
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Получает список всех пожертвований для текущего пользователя."""
    reservations = await donation_crud.get_by_user(session=session, user=user)
    return reservations
