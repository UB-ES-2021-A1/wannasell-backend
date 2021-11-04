from rest_framework import serializers

from products.models import Category, Product, Image


class ProductSellerSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=500)


class ProductDataSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=500, allow_blank=False)
    description = serializers.CharField(max_length=1000, allow_blank=True)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    category_name = serializers.CharField(source='category.name')
    category_description = serializers.CharField(source='category.get_name_display')
    thumbnail = serializers.SerializerMethodField("get_thumbnail")
    seller = ProductSellerSerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'seller', 'thumbnail', 'category_name', 'category_description']

    def get_thumbnail(self, obj):
        images = Image.objects.filter(product=obj)
        if len(images) > 0:
            return images.first().image.url
        return None

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
