from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation, User
from app.schemas.charity_project import CharityProjectUpdate


async def check_invested_amount_not_zero(
        project_id: int,
        session: AsyncSession,
) -> None:
    project = await project_crud.get(project_id, session)
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    return project


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проекта с таким id не существует!'
        )
    return project


async def check_project_not_closed(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await project_crud.get(project_id, session)
    if project.fully_invested == 1:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )
    return project


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project = await project_crud.get_project_by_name(project_name, session)
    if project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Проект с таким именем уже существует!"
        )


async def check_full_amount_greater_than_invested(
    project: CharityProject,
    obj_in: CharityProjectUpdate
) -> None:
    if project.invested_amount > obj_in.full_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=(
                "Общая сумма по проекту должна "
                "всегда быть больше уже инвестированной!"
            )
        )
