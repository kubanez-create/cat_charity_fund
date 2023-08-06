from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount_greater_than_invested,
    check_invested_amount_not_zero,
    check_name_duplicate,
    check_project_exists,
    check_project_not_closed,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investment import invest

router = APIRouter()


@router.post(
    "/",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(project.name, session)
    new_project = await project_crud.create(project, session)
    new_project = await invest(project=new_project, session=session)
    return new_project


@router.get(
    "/",
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Доступно для всех."""
    all_projects = await project_crud.get_multi(session)
    return all_projects


@router.patch(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_not_closed(project_id, session)
    project = await check_project_exists(project_id, session)
    if obj_in.full_amount is not None:
        await check_full_amount_greater_than_invested(project, obj_in)
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    meeting_room = await project_crud.update(project, obj_in, session)
    return meeting_room


@router.delete(
    "/{project_id}",
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exists(project_id, session)
    project = await check_invested_amount_not_zero(project_id, session)
    project = await project_crud.remove(project, session)
    return project
