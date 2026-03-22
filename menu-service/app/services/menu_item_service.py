from typing import List, Optional
from beanie import PydanticObjectId
from app.models.menu_item import MenuItem
from app.models.item import Item
from app.schemas.menu_item import MenuItemCreate, MenuItemUpdate, MenuItemDetailResponse


async def get_all() -> List[MenuItem]:
    return await MenuItem.find_all().to_list()


async def get_by_id(menu_item_id: str) -> Optional[MenuItem]:
    try:
        return await MenuItem.get(PydanticObjectId(menu_item_id))
    except Exception:
        return None


async def create(data: MenuItemCreate) -> MenuItem:
    menu_item = MenuItem(**data.model_dump())
    await menu_item.insert()
    return menu_item


async def update(menu_item_id: str, data: MenuItemUpdate) -> Optional[MenuItem]:
    menu_item = await get_by_id(menu_item_id)
    if not menu_item:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(menu_item, field, value)
    await menu_item.save()
    return menu_item


async def delete(menu_item_id: str) -> bool:
    menu_item = await get_by_id(menu_item_id)
    if not menu_item:
        return False
    await menu_item.delete()
    return True


async def get_items_in_menu(menu_id: str) -> List[MenuItemDetailResponse]:
    menu_items = await MenuItem.find(MenuItem.menu_id == menu_id).to_list()
    results = []
    for mi in menu_items:
        item_doc: Optional[Item] = None
        try:
            item_doc = await Item.get(PydanticObjectId(mi.item_id))
        except Exception:
            pass
        results.append(
            MenuItemDetailResponse(
                id=str(mi.id),
                menu_id=mi.menu_id,
                availability=mi.availability,
                created_at=mi.created_at,
                item=item_doc,
            )
        )
    return results
