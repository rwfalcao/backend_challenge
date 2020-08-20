from django.core.management.base import BaseCommand
from car_management.models import EventType

class Command(BaseCommand):
    help = "Populate database with options provided in EventType.INITIAL_EVENTS"

    def handle(self, *args, **options):
        for event_id, event_description in EventType.INITIAL_EVENTS:
            event_type = EventType.objects.filter(
                id=event_id
            ).first()
            if event_type:
                print('An event type already exists with id %s with the description of: "%s". Manual data manipulation may be required required.' % (event_type.id, event_type.description))
            else:
                EventType.objects.create(
                    id=event_id,
                    description=event_description
                )