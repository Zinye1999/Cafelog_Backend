from django.db import models
from utils.model import BaseJsonModel

class CafeReview(BaseJsonModel):

    review = models.TextField(blank=True, null=True)
    reviewer = models.ForeignKey("User", on_delete=models.DO_NOTHING)
    pictures = models.JSONField(blank=True, null=True, default=list)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    class Meta:
        db_table = "cafe_reviews"
        verbose_name = "cafe_review"