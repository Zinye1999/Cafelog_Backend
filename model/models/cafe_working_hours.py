from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.model import BaseJsonModel
from utils.fields import TextChoices

class Days(TextChoices):
    SUN = "0", _("Sunday")
    MON = "1", _("Monday")
    TUE = "2", _("Tuesday")
    WED = "3", _("Wednesday")
    THU = "4", _("Thursday")
    FRI = "5", _("Friday")
    SAT = "6", _("Saturday")
    
DAYS_CHOICES = Days.choices_dict()

class CafeWorkingHours(BaseJsonModel):

    day_of_week = models.CharField(max_length=1, choices=Days.choices)
    start = models.TimeField()
    end = models.DurationField()
    
    class Meta:
        db_table = "cafe_working_hours"
        verbose_name = "cafe_working_hours"
        ordering = ("day_of_week", )