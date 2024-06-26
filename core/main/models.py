# dishsearch/models.py
from django.db import models
import json

class Dish(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    items = models.JSONField(null=True, blank=True)  # Use JSONField to store JSON data
    lat_long = models.CharField(max_length=255, null=True, blank=True)
    full_details = models.JSONField(null=True, blank=True)  # Use JSONField to store JSON data

    def __str__(self):
        return self.name

    def set_items(self, items):
        self.items = json.dumps(items)

    def get_items(self):
        return json.loads(self.items)

    def set_full_details(self, details):
        self.full_details = json.dumps(details)

    def get_full_details(self):
        return json.loads(self.full_details)
