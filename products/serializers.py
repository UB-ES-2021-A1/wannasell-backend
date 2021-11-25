from rest_framework import serializers

from favorites.models import Favorites
from products.models import Category, Product, Image


class ProductSellerSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=500)
    products = serializers.SerializerMethodField('get_products')

    def get_products(self, obj):
        products = Product.objects.filter(seller=obj)
        count = products.count()
        return count

class ProductDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=500, allow_blank=False)
    description = serializers.CharField(max_length=1000, allow_blank=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    category_name = serializers.CharField(source='category.name')
    category_description = serializers.CharField(source='category.get_name_display')
    thumbnail = serializers.SerializerMethodField("get_thumbnail")
    seller = ProductSellerSerializer()
    favorites_count = serializers.SerializerMethodField('get_favorites_count')
    favorites = serializers.SerializerMethodField('get_favs')
    views = serializers.IntegerField()
    created_at = serializers.DateTimeField(format="%d-%b-%Y")


    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'seller', 'thumbnail', 'category_name', 'category_description',
                  'favorites_count', 'favorites', 'views', 'created_at']

    def get_thumbnail(self, obj):
        images = Image.objects.filter(product=obj)
        if len(images) > 0:
            return images.first().image.url
        return None

    def get_favorites_count(self, obj):
        fav_list = Favorites.objects.filter(product=obj)
        count = fav_list.count()
        return count

    def get_favs(self, obj):
        fav_list = Favorites.objects.filter(product=obj)
        return fav_list.values_list('user__username', flat=True)


class CategoryDataSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=2)

    class Meta:
        model = Category
        fields = ['name']


class ImageDataSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(allow_null=False)

    class Meta:
        model = Image
        fields = ['image']
