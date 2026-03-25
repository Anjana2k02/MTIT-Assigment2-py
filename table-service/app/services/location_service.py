from typing import List, Optional
from beanie import PydanticObjectId
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate


async def get_all() -> List[Location]:
    return await Location.find_all().to_list()


async def get_by_id(location_id: str) -> Optional[Location]:
    try:
        return await Location.get(PydanticObjectId(location_id))
    except Exception:
        return None


async def create(data: LocationCreate) -> Location:
    location = Location(**data.model_dump())
    await location.insert()
    return location


async def update(location_id: str, data: LocationUpdate) -> Optional[Location]:
    location = await get_by_id(location_id)
    if not location:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(location, field, value)
    await location.save()
    return location


async def delete(location_id: str) -> bool:
    location = await get_by_id(location_id)
    if not location:
        return False
    await location.delete()
    return True
