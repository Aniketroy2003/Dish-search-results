# dishsearch/management/commands/import_dishes.py
import csv
import json
from django.core.management.base import BaseCommand
from main.models import Dish

class Command(BaseCommand):
    help = 'Import dish details from CSV'

    def handle(self, *args, **kwargs):
        file_path = 'main/restaurants_small.csv'  # Adjust this path as per your file location

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                dish_name = row.get('name', '').strip()
                if not dish_name:
                    self.stdout.write(self.style.WARNING(f'Skipping row with missing dish name: {row}'))
                    continue

                location = row.get('location', '').strip()
                items_str = row.get('items', '{}').strip()
                items = json.loads(items_str) if items_str else {}

                lat_long = row.get('lat_long', '').strip()
                full_details_str = row.get('full_details', '{}').strip()
                full_details = json.loads(full_details_str) if full_details_str else {}

                Dish.objects.create(
                    name=dish_name,
                    location=location,
                    items=items,
                    lat_long=lat_long,
                    full_details=full_details
                )

        self.stdout.write(self.style.SUCCESS('Successfully imported dish details'))
