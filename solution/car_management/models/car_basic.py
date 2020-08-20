from django.db import models
import numbers

from car_management.managers import TyreManager


class Car (models.Model):

    MIN_REFUEL_CAPACITY = 5
    MAX_NUMBER_OF_TYRES = 4

    current_gas_level = models.DecimalField(
        'Gas level in %',
        default=0,
        max_digits=3, 
        decimal_places=2
    )

    gas_capacity = models.IntegerField(
        'Gas capacity in Liters',
    )

    @classmethod
    def is_missing_tyre():
        '''
            Returns whether or not the car is missing at least one tyre.
        '''

        amout_tyres_in_use = self.tyre_set.amount_in_use()
        if amout_tyres_in_use <= self.MAX_NUMBER_OF_TYRES:
            return True

        return False

    def refuel(self, amount):
        '''
            Increases car's object gas capacity by the amount received in liters.

            :param float amount: Amount of liters of fuel to be added to the car.
        '''

        amount_is_number = isinstance(amount, numbers.Number)
        if amount_is_number:
            wont_overflow = amount + self.current_gas_level <= gas_capacity

            if wont_overflow:
                self.current_gas_level += amount
                self.save()
                return self.current_gas_level

        return None

    def maintenance(self, part):
        '''
            Method responsible for calling subroutines for car maintenance.

            :param str part: Text representing one of the possible parts to be replace found in Car.REPLACEABLE_PARTS.
        '''

        if isinstance(part, str):
            part = part.lower()

            if part == 'tyre':
                self.replace_degraded_tyres()

    def add_new_tyre(self):
        '''
            Method responsible adding a new tyre to the car.
        '''
        if self.is_missing_tyre:
            return Tyre.objects.create(
                car=self,
                currently_in_use=True
            )
        return None


    def replace_degraded_tyres(self):
        '''
            Replace all tyres that are above their degradation limit.
        '''

        replaceable_tyres = self.tyre_set.replaceable()

        for tyre in replaceable_tyres:
            tyre.replace()

    def get_status(self):
        '''
            TODO: Every info about the car
        '''

class Tyre (models.Model):

    objects = TyreManager()

    DEGRADATION_RATE= 3         # 3KM -> 1% DEGRADATION
    DEGRADATION_LIMIT = 94      # 94% MAX DEGRADATION BEFORE A TYRE CAN BE SWAPPED

    degradation = models.DecimalField(
        'Tyre Degradation in %',
        default=0,
        max_digits=9, 
        decimal_places=2
    )

    car = models.ForeignKey(
        'car_management.Car', 
        on_delete=models.CASCADE
        )

    currently_in_use = models.BooleanField(
        default=False
    )
    
    def __str__(self):
        if self.car:
            return "Car %s's tyre" % self.car.id
        return "Available tyre"

    def replace(self):
        self.currently_in_use = False
        self.save()

        car = self.car
        car.add_tyre()


class Trip (models.Model):

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