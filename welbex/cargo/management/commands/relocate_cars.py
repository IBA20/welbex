from django.core.management.base import BaseCommand
from random import choice

from cargo.models import Car, Location


class Command(BaseCommand):
    def handle(self, *args, **options):
        all_zips = Location.objects.only('zip')
        cars = Car.objects.all()
        for car in cars:
            car.location = choice(all_zips)

        Car.objects.bulk_update(cars, fields=['location'])
