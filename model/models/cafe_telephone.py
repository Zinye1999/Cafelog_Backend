from django.db import models
from utils.model import BaseJsonModel

class CafeTelephone(BaseJsonModel):

    number = models.CharField(max_length=10) # thailand telephone number
    details = models.CharField(max_length=150, blank=True, null=True)
    
    class Meta:
        db_table = "cafe_telephones"
        verbose_name = "cafe_telephone"