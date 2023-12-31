from datetime import datetime
from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.crud.charity_project import project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


async def dole_out(
    *,
    container: Union[CharityProject, Donation],
    item: Union[CharityProject, Donation],
    crud_func: CRUDBase,
    session: AsyncSession
):
    """Change database objects according to a new donation or project.

    Args:
        container (Union[CharityProject, Donation]): added object
        item (Union[CharityProject, Donation]): added donation
        crud_func (CRUDBase): crud function
        session (AsyncSession): session object

    Returns:
        container (Union[CharityProject, Donation]): added object
    """
    items = await crud_func.get_active(session=session)
    if not items:
        return container
    famount = container.full_amount
    for item_obj in items:
        money_left = item_obj.full_amount - item_obj.invested_amount
        if money_left < famount:
            container.invested_amount += money_left
            item_obj.invested_amount += money_left
            item_obj.fully_invested = True
            item_obj.close_date = datetime.utcnow()
            famount -= money_left
        elif money_left == famount:
            container.invested_amount += money_left
            item_obj.invested_amount += item_obj.full_amount
            item_obj.fully_invested = True
            item_obj.close_date = datetime.utcnow()
            container.fully_invested = True
            container.close_date = datetime.utcnow()
            break
        else:
            container.invested_amount += famount
            container.fully_invested = True
            container.close_date = datetime.utcnow()
            item_obj.invested_amount += famount
            break
        session.add_all([container, item_obj])
    await session.commit()
    await session.refresh(container)
    return container


async def invest(
    *, project: CharityProject = None,
    don_obj: Donation = None,
    session: AsyncSession
) -> Union[None, CharityProject, Donation]:
    """Change databade objects according to a new one.

    Args:
        session (AsyncSession): session object
        project (CharityProject, optional): added project. Defaults to None.
        don_obj (Donation, optional): added donation. Defaults to None.

    Returns:
        Union[None, CharityProject, Donation]: added object
    """
    if project is not None:
        return await dole_out(
            container=project,
            item=don_obj,
            crud_func=donation_crud,
            session=session
        )

    if don_obj is not None:
        return await dole_out(
            container=don_obj,
            item=project,
            crud_func=project_crud,
            session=session
        )
