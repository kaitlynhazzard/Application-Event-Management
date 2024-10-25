from fastapi import APIRouter, HTTPException

from app.models.event import Event
from app.resources.event_resource import EventResource
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.get("/events/{EID}", tags=["events"])
async def get_events(eid: str) -> Event:
    # TODO Do lifecycle management for singleton resource
    res = ServiceFactory.get_service("EventResource")
    result = res.get_by_key(eid)
    return result


@router.get("/events", tags=["events"])
async def get_events():
    # Get the database service
    eve_resource = EventResource(config=None)

    # Test database connection with a simple query
    try:
        result = eve_resource.get_all_events()
        return {"status": "connected", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection failed: {str(e)}")


@router.post("/events/{EID}", tags=["event"])
async def create_event(event: Event):
    eve_resource = EventResource(config=None)
    try:
        success = eve_resource.insert_event(event)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to create the event")
        return {"message": "Event created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Event creation failed: {str(e)}")


@router.put("/events/{EID}", tags=["event"])
async def update_event(eid: str, event: Event):
    eve_resource = EventResource(config=None)
    try:
        success = eve_resource.update_event(eid, event)
        if not success:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"message": "Event updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Event update failed: {str(e)}")


@router.delete("/events/{EID}", tags=["event"])
async def delete_event(eid: str):
    eve_resource = EventResource(config=None)
    try:
        success = eve_resource.delete_event(eid)
        if not success:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"message": "Event deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Event deletion failed: {str(e)}")