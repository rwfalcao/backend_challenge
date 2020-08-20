from django.db import models

class Car (models.Model):
    '''
        TODO: comment
    '''

    MIN_REFUEL_CAPACITY = 5
    MAX_NUMBER_OF_TYRES = 4

    gas_capacity = models.DecimalField(
        'Gas capacity in %',
        max_digits=3, 
        decimal_places=2
    )


class Tyre (models.Model):
    '''
        TODO: comment
    '''

    DEGRADATION_RATE= 3         # 3KM -> 1% DEGRADATION
    DEGRADATION_LIMIT = 94      # 94% MAX DEGRADATION BEFORE A TYRE CAN BE SWAPPED

    degradation = models.DecimalField(
        'Tyre Degradation in %',
        max_digits=3, 
        decimal_places=2
    )

    car = models.ForeignKey(
        'car_management.Car', 
        on_delete=models.CASCADE
        )
    
    def __str__(self):
        if self.car:
            return "Car %s's tyre" % self.car.id
        return "Available tyre"


class Trip (models.Model):
    '''
        TODO: comment
    '''

    car = models.ForeignKey(
        'car_management.Car', 
        on_delete=models.CASCADE
        )
        
    distance = models.DecimalField(
        'Distance traveled in KM',
        max_digits=9, 
        decimal_places=2
    )


    def __str__(self):
        return '%s km trip by car %s' % (self.distance, self.car.id)


class Event (models.Model):
    '''
        TODO: comment
    '''

    trip = models.ForeignKey(
        'car_management.EventType', 
        on_delete=models.CASCADE
        )

    km = models.DecimalField(
        'KM which the event happened',
        max_digits=9, 
        decimal_places=2
    )


    

class EventType (models.Model):
    '''
        TODO: comment
    '''

    INITIAL_EVENTS = [
        (1, 'Tyre Change'),
        (2, 'Refuel')
    ]

    description = models.CharField(
        'Event Description',
        max_length=100,
        null=False
        )

    def __str__(self):
        return self.description