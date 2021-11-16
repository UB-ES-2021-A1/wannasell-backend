from rest_framework import serializers

from products.models import Category, Product, Image
from favorites.models import Favorites


class FavDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['id', 'user', 'product']
