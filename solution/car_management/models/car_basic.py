from django.db import models

from car_management.managers import TyreManager
from car_management.utils import *


class Car (models.Model):

    MIN_REFUEL_CAPACITY = 5
    MAX_NUMBER_OF_TYRES = 4
    KMS_PER_LITER = 8

    current_gas_level = models.DecimalField(
        'Liters in gas tank',
        default=0,
        max_digits=3, 
        decimal_places=2
    )

    gas_capacity = models.IntegerField(
        'Gas capacity in Liters',
    )

    def travel(self, distance):
        '''
            Reflects all possible changes to car value due to a travel.

            :param float distance: Distance travelled in KM .
        '''
        
        self.degrade_tyres(distance)
        self.consume_fuel(distance)

    def degrade_tyres(self, distance):
        '''
            Decrease current gas level relative to the distance travelled.

            :param float distance: Distance travelled in KM .
        '''

        for tyre in self.tyre_set.in_use():
            tyre.degrade(distance)

    def consume_fuel(self, distance):
        '''
            Decrease current gas level relative to the distance travelled.

            :param float distance: Amount of liters of fuel to be added to the car.
        '''

        self.current_gas_level -= distance / Car.KMS_PER_LITER
        self.save()

    def refuel(self, amount):
        '''
            Increases car's object gas level by the amount received in liters.

            :param float amount: Amount of liters of fuel to be added to the car.
        '''

        amount_is_number = is_number(amount)
        if amount_is_number:
            wont_overflow = amount + self.current_gas_level <= gas_capacity

            if wont_overflow:
                self.current_gas_level += amount
                self.save()
                return self.current_gas_level

        return None

    def get_refuel_amount(self):
        '''
            Returns refuel amount in liters so the tank is full.
        '''

        capacity = self.gas_capacity
        current_gas_level = self.current_gas_level

        return capacity - current_gas_level
    
    def replenish_gas_tank(self):
        '''
            Adds the amount of fuel the car needs for the tank to be full.
        '''

        amount_gas_needed = self.get_refuel_amount()

        return self.refuel(amount_gas_needed)

    def maintenance(self, event_id):
        '''
            Method responsible for calling subroutines for car maintenance.

            :param int event_id: Id of one of the possible events that require some type of maintenance during a trip.
        '''

        if event_type_id == EventType.TYRE_CHANGE_ID:
            self.replace_degraded_tyres()
            return True
        elif event_type_id == EventType.REFUEL_ID:
            self.replenish_gas_tank()
            return True

        return False

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

    def get_current_tank_milage(self):
        '''
            Returns max trip distance with current gas level in KM.
        '''

        return self.current_gas_level * self.KMS_PER_LITER

    def get_km_before_tyre_change(self):
        '''
            Return how many kimoleters the most used tyre has left for use.
        '''
        most_used_tyre = self.tyre_set.in_use().order_by(
            '-degradation'
        ).first()

        if most_used_tyre:
           tyre_lifespan = most_used_tyre.get_lifespan()

           return tyre_lifespan * Tyre.DEGRADATION_RATE

    def get_next_maintenance_stop(self):
        '''
            Return the distance before the next stop for either tyre change or refuel.
        '''

        next_tyre_change_in = self.get_km_before_tyre_change()
        current_tank_milage = self.get_current_tank_milage()

        next_maintenance = min([next_tyre_change_in, current_tank_milage])

        return next_maintenance, next_tyre_change_in, current_tank_milage

    def get_status(self):
        '''
            TODO: Every info about the car
        '''
        pass

    @classmethod
    def is_missing_tyre():
        '''
            Returns whether or not the car is missing at least one tyre.
        '''

        amout_tyres_in_use = self.tyre_set.amount_in_use()
        if amout_tyres_in_use <= self.MAX_NUMBER_OF_TYRES:
            return True

        return False

class Tyre (models.Model):

    objects = TyreManager()

    DEGRADATION_RATE = 3            # 3KM -> 1% DEGRADATION
    DEGRADATION_THRESHOLD = 94      # 94% MAX DEGRADATION BEFORE A TYRE CAN BE SWAPPED
    DEGRADATION_LIMIT = 99

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

    def get_lifespan(self):
        ''' 
            Method responsible for returning the % left on the tyre's lifespan.
        '''

        percentage_left = Tyre.DEGRADATION_LIMIT - most_used_tyre.degradation
        return percentage_left if percentage_left >= 0 else 0

    def replace(self):
        ''' 
            Method responsible for replacing the object's tyre.
        '''
        self.currently_in_use = False
        self.save()

        car = self.car
        car.add_new_tyre()
    
    def degrade(self, distance):
        ''' 
            Method responsible for updating tyre's degrade percentage based on a distance.

            :param float distance: Distance travelled in KM .
        '''

        self.degradation += distance * Tyre.DEGRADATION_RATE
        self.save()


class Trip (models.Model):

    car = models.ForeignKey(
        'car_management.Car', 
        on_delete=models.CASCADE
        )
        
    distance = models.DecimalField(
        'Total distance to be traveled in KM',
        max_digits=9, 
        decimal_places=2
    )

    travelled_distance = models.DecimalField(
        'Distance traveled in KM',
        max_digits=9, 
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return '%s km trip by car %s' % (self.distance, self.car.id)

    def new_event(self, km, event_type_id):
        '''
            Creates new event that happened during the trip.
        '''

        try:
            event_type = EventType.objects.get(id=event_type_id)
        except:
            event_type = None

        if event_type:
            event = Event.objects.create(
                trip=self,
                event_type=event_type,
                km=km
            )
            return event

        return None

    def start(self):
        '''
            Routine that simulates what happened during the trip.
        '''

        while not self.has_arrived_at_destination():
            next_stop_in, tyre_change_in, refuel_in = self.car.get_next_maintenance_stop()

            if self.stop_needed_before_destination(next_stop_in):
                self.travelled_distance += next_stop_in

                self.car.travel(next_stop_in)

                event_type_id = EventType.TYRE_CHANGE_ID if tyre_change_in < refuel_in else EventType.REFUEL_ID

                self.car.maintenance(event_type_id)

                event = self.new_event(
                    km=self.travelled_distance,
                    event_type_id=event_type_id
                )
    
    def has_arrived_at_destination(self):
        '''
            Returns whether or not the car has reached it's final destination on this Trip.
        '''

        return True if self.travelled_distance >= self.distance else False

    def stop_needed_before_destination(self, next_stop_distance=None):
        '''
            Returns whether or not the car will need maintenance before the end of the Trip. 
            Calling the method without a distance as an argument will return if the car will
            need to stop at all until the end of the trip.

            :param float next_stop_distance: Distance in KM needed for the next maintenance stop.
        '''

        if not next_stop_distance:
            next_stop_distance = self.distance
        
        distance_to_stop = next_stop_distance + self.travelled_distance

        return True if distance_to_stop < self.distance else False


class Event (models.Model):

    trip = models.ForeignKey(
        'car_management.Trip', 
        on_delete=models.CASCADE
        )

    event_type = models.ForeignKey(
        'car_management.EventType', 
        on_delete=models.CASCADE
        )

    km = models.DecimalField(
        'KM which the event happened',
        max_digits=9, 
        decimal_places=2
    )

    def __str__(self):
        return '%s on Trip (%s)' % (self.event_type.description, self.trip.id)


class EventType (models.Model):

    TYRE_CHANGE_ID = 1
    REFUEL_ID = 2

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