from django.db import models
from django.apps import apps


class TyreManager(models.Manager):
    

    def get_queryset(self):
        return super().get_queryset().all()

    def in_use(self):
        return self.get_queryset().filter(
            currently_in_use=True
        )

    def amount_in_use(self):
        return self.get_queryset().filter(
            currently_in_use=True
        ).count()

    def replaceable(self):
        tyre_model = apps.get_model(app_label='car_management', model_name='Tyre')
        return self.in_use().filter(
           degradation__gt=tyre_model.DEGRADATION_LIMIT
        )
    
    def discarded(self):
        tyre_model = apps.get_model(app_label='car_management', model_name='Tyre')
        return self.filter(
            currently_in_use=False,
            degradation__gt=tyre_model.DEGRADATION_LIMIT
        )
