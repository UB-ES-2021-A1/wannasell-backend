from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Favorites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorites')
