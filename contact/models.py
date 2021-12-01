from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Contact(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_buyer')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contact_seller')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='contact_product')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['buyer', 'seller', 'product'], name='unique_contact')
        ]
