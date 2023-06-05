import csv
from random import randint, choice
from django.db import migrations


def import_locations(apps, schema_editor):
    Location = apps.get_model('cargo', 'Location')
    with open('uszips.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        location_entries = []
        for row in reader:
            location_entries.append(
                Location(
                    zip=row['zip'],
                    lat=row['lat'],
                    lon=row['lng'],
                    city=row['city'],
                    state=row['state_name'],
                )
            )

        Location.objects.bulk_create(
            location_entries,
            batch_size=999,
            update_conflicts=True,
            update_fields=['lat', 'lon', 'city', 'state'],
            unique_fields=['zip'],
        )


def create_random_cars(apps, schema_editor):
    Car = apps.get_model('cargo', 'Car')
    Location = apps.get_model('cargo', 'Location')
    all_zips = Location.objects.only('zip')
    if Car.objects.count() >= 20:
        return
    car_entries = []
    for _ in range(20):
        location = choice(all_zips)
        car_entries.append(
            Car(
                number=f'{randint(1000, 9999)}'
                       f'{choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}',
                location=location,
                carrying=randint(1, 10) * 100
            )
        )

    Car.objects.bulk_create(
        car_entries,
        ignore_conflicts=True,
        unique_fields=['number'],
    )


class Migration(migrations.Migration):

    dependencies = [
        ('cargo', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(import_locations),
        migrations.RunPython(create_random_cars),
    ]
