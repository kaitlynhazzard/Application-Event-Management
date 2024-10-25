from fastapi import APIRouter, HTTPException

from app.models.event import Event
from app.resources.event_resource import EventResource
from app.services.service_factory import ServiceFactory

router = APIRouter()


@router.get("/eve_tab/{EID}", tags=["users"])
async def get_events() -> Event:
    eid = "E001"
    print("AAAAA", eid)
    # TODO Do lifecycle management for singleton resource
    res = ServiceFactory.get_service("EventResource")
    result = res.get_by_key(eid)
    return result


@router.post("/eve_tab", response_model=Event, tags=["events"])
async def create_event(event: Event):
    """
    Create a new event.
    """
    print("AAAAABBBBB")
    # Get the EventResource service
    res = ServiceFactory.get_service("EventResource")

    # Save the event using the data service
    try:
        result = res.insert_event(event)
        if result:
            return event
        else:
            raise HTTPException(status_code=500, detail="Event creation failed.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))