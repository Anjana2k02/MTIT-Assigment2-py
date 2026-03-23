from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas.location import LocationCreate, LocationUpdate, LocationResponse
from app.services import location_service

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=List[LocationResponse])
async def get_locations():
    return await location_service.get_all()


@router.get("/{location_id}", response_model=LocationResponse)
async def get_location(location_id: str):
    location = await location_service.get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@router.post("/", response_model=LocationResponse, status_code=201)
async def create_location(data: LocationCreate):
    return await location_service.create(data)


@router.put("/{location_id}", response_model=LocationResponse)
async def update_location(location_id: str, data: LocationUpdate):
    updated = await location_service.update(location_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Location not found")
    return updated


@router.delete("/{location_id}", status_code=204)
async def delete_location(location_id: str):
    deleted = await location_service.delete(location_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Location not found")
