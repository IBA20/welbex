from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.conf import settings
from geopy import distance


class Location(models.Model):
    zip = models.PositiveIntegerField(
        'Индекс',
        validators=[MinValueValidator(100), MaxValueValidator(99999)],
        primary_key=True,
    )
    city = models.CharField('Город', max_length=40)
    state = models.CharField('Штат', max_length=30)
    lat = models.DecimalField(
        'Широта',
        max_digits=7,
        decimal_places=5,
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    lon = models.DecimalField(
        'Долгота',
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )

    def __str__(self):
        return f'{self.zip} {self.city}, {self.state}'


class ShipmentQuerySet(models.QuerySet):
    def with_cars_nearby(
            self,
            radius=settings.CARS_LOOKUP_RADIUS_MI,
            min_weight=None,
            max_weight=None,
    ):
        all_cars = Car.objects.select_related('location')
        shipments = self.select_related('pick_up', 'delivery')
        if min_weight:
            shipments = shipments.filter(weight__gte=float(min_weight))
        if max_weight:
            shipments = shipments.filter(weight__lte=float(max_weight))
        for shipment in shipments:
            cars_nearby = sum(1 if distance.distance(
                (shipment.pick_up.lat, shipment.pick_up.lon),
                (car.location.lat, car.location.lon)
            ).mi <= int(radius) and shipment.weight <= car.carrying
                              else 0 for car in all_cars)
            shipment.cars_nearby = cars_nearby
        return shipments


class Shipment(models.Model):
    pick_up = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='pick_ups',
        verbose_name='Локация отправки',
        null=True,
    )
    delivery = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='deliveries',
        verbose_name='Локация доставки',
        null=True,
    )
    weight = models.PositiveSmallIntegerField(
        'Вес',
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        db_index=True,
    )
    description = models.TextField('Описание', blank=True)

    objects = ShipmentQuerySet.as_manager()

    def __str__(self):
        return f'{self.pick_up} - {self.delivery}, {self.weight}kg'


class CarQuerySet(models.QuerySet):
    def get_numbers_with_distances(self, lat, lon):
        cars = self.select_related('location')
        numbers_with_distances = [
            {
                'number': car.number,
                'distance':  distance.distance(
                    (car.location.lat, car.location.lon),
                    (lat, lon),
                ).mi
             } for car in cars]
        return numbers_with_distances


class Car(models.Model):
    number = models.CharField(
        'Номер',
        max_length=5,
        db_index=True,
        unique=True,
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='cars',
        verbose_name='Текущая локация',
        null=True,
    )
    carrying = models.PositiveSmallIntegerField(
        'Грузоподъемность',
        validators=[MinValueValidator(1), MaxValueValidator(1000)],
        db_index=True,
    )

    objects = CarQuerySet.as_manager()

    def __str__(self):
        return f'{self.number}, {self.carrying}kg'
