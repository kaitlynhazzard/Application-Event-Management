from typing import Any

from framework.resources.base_resource import BaseResource

from app.models.event import Event
from app.services.service_factory import ServiceFactory


class EventResource(BaseResource):

    def __init__(self, config):
        super().__init__(config)

        # TODO -- Replace with dependency injection.
        #
        self.data_service = ServiceFactory.get_service("EventResourceDataService")
        self.database = "EVENTS"
        self.collection = "eve_tab"
        self.key_field="EID"
        # TODO -- foreign key

    def get_by_key(self, key: str) -> Event:

        d_service = self.data_service

        result = d_service.get_data_object(
            self.database, self.collection, key_field=self.key_field, key_value=key
        )

        result = Event(**result)
        return result

    def get_all_events(self):
        data_service = self.data_service
        result = data_service.check_connection(self.database, self.collection)
        return result

    def insert_event(self, event: Event) -> bool:
        """
        Inserts a new event into the database.

        Args:
            event (Event): The event object to be inserted.

        Returns:
            bool: True if the event was inserted successfully.
        """
        # Convert the Event object to a dictionary
        event_data = event.model_dump()

        # Call the data service's insert method
        result = self.data_service.insert_data_object(
            self.database, self.collection, event_data
        )

        return result

