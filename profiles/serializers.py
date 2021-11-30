from rest_auth.serializers import serializers

from favorites.models import Favorites
from products.models import Product


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=500)


class ProfileDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    avatar = serializers.ImageField(allow_null=False)
    bio = serializers.CharField(max_length=500, allow_blank=True)
    address = serializers.CharField(max_length=1024, allow_blank=True)
    location = serializers.CharField(max_length=100, allow_blank=True)
    fav_count = serializers.SerializerMethodField('fav_count')
    favs = serializers.SerializerMethodField('fav_list')
    products = serializers.SerializerMethodField('products_count')
    user = UserSerializer()
    phone = serializers.CharField(max_length=12, allow_blank=True)

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.address = validated_data.get('address', instance.address)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance

    def fav_count(self, obj):
        fav_list = Favorites.objects.filter(user=obj.user)
        count = fav_list.count()
        return count

    def fav_list(self, obj):
        fav_list = Favorites.objects.filter(user=obj.user)
        return fav_list.values_list('product__id', flat=True)

    def products_count(self, obj):
        products = Product.objects.filter(seller=obj.user)
        count = products.count()
        return count
