from django.contrib.auth.models import User
from django.db import models

class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller')
    message = models.TextField()
    val = models.IntegerField()
    check = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['reviewer', 'seller'], name='unique_review')
        ]