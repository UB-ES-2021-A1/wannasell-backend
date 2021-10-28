from rest_framework import serializers
from django.contrib.auth.models import User
from products.models import Category, Product, Image
from django.db import models


class ProductDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=500, allow_blank=False)
    description = serializers.CharField(max_length=1000, allow_blank=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # seller = serializers.(User, on_delete=models.CASCADE, null=True)
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'seller', 'category_name']


class CategoryDataSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=2)


    class Meta:
        model = Category
        fields = ['name']


class ImageDataSerializer(serializers.ModelSerializer):
    product = ProductDataSerializer()
    image = serializers.ImageField(allow_null=False)

    class Meta:
        model = Image
        fields = ['id', 'product', 'image']
