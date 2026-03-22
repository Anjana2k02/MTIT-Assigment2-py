from typing import List, Optional
from beanie import PydanticObjectId
from app.models.menu import Menu
from app.schemas.menu import MenuCreate, MenuUpdate


async def get_all() -> List[Menu]:
    return await Menu.find_all().to_list()


async def get_by_id(menu_id: str) -> Optional[Menu]:
    try:
        return await Menu.get(PydanticObjectId(menu_id))
    except Exception:
        return None


async def create(data: MenuCreate) -> Menu:
    menu = Menu(**data.model_dump())
    await menu.insert()
    return menu


async def update(menu_id: str, data: MenuUpdate) -> Optional[Menu]:
    menu = await get_by_id(menu_id)
    if not menu:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(menu, field, value)
    await menu.save()
    return menu


async def delete(menu_id: str) -> bool:
    menu = await get_by_id(menu_id)
    if not menu:
        return False
    await menu.delete()
    return True
