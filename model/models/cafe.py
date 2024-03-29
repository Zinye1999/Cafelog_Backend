from django.db import models
from utils.model import BaseJsonModel
from decimal import Decimal

class Cafe(BaseJsonModel):

    name = models.CharField(max_length=150, default="")
    picture = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    tags = models.TextField(blank=True, null=True)

    # latitude and longitude chiang mai from google maps
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=Decimal('18.7942459'))
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=Decimal('98.9564772'))
    address = models.TextField(blank=True, null=True)
    telephones = models.ManyToManyField("CafeTelephone")
    working_hours = models.ManyToManyField("CafeWorkingHours")
    reviews = models.ManyToManyField("CafeReview")
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)

    class Meta:
        db_table = "cafes"
        verbose_name = "cafe"