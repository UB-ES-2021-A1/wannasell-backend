from django.db.models import Q, Avg
from rest_auth.serializers import serializers

from favorites.models import Favorites
from products.models import Product
from reviews.models import Review


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=500)


class ProfileDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    avatar = serializers.ImageField(allow_null=False)
    bio = serializers.CharField(max_length=500, allow_blank=True)
    address = serializers.CharField(max_length=1024, allow_blank=True)
    location = serializers.CharField(max_length=100, allow_blank=True)
    phone = serializers.CharField(max_length=24, allow_blank=True)
    countryCallingCode = serializers.CharField(max_length=5, allow_blank=True)
    countryCode = serializers.CharField(max_length=2, allow_blank=True)
    formatInternational = serializers.SerializerMethodField('get_phone_international')
    fav_count = serializers.SerializerMethodField('favs_count')
    favs = serializers.SerializerMethodField('fav_list')
    products = serializers.SerializerMethodField('products_count')
    user = UserSerializer()
    n_sold_products = serializers.SerializerMethodField('sold_products')
    n_selling_products = serializers.SerializerMethodField('selling_products')
    n_favorite_products = serializers.SerializerMethodField('favorite_products')
    n_user_reviews = serializers.SerializerMethodField('user_reviews')
    review_mean = serializers.SerializerMethodField('user_review_mean')

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.address = validated_data.get('address', instance.address)
        instance.location = validated_data.get('location', instance.location)
        instance.phone = validated_data.get('phone', instance.location)
        instance.countryCallingCode = validated_data.get('countryCallingCode', instance.location)
        instance.countryCode = validated_data.get('countryCode', instance.location)
        instance.save()
        return instance

    def favs_count(self, obj):
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

    def selling_products(self, obj):
        products = Product.objects.filter(Q(seller=obj.user) & Q(sold=False))
        count = products.count()
        return count

    def sold_products(self, obj):
        products = Product.objects.filter(Q(seller=obj.user) & Q(sold=True))
        count = products.count()
        return count

    def favorite_products(self, obj):
        products = Favorites.objects.filter(Q(user=obj.user))
        count = products.count()
        return count

    def user_reviews(self, obj):
        reviews = Review.objects.filter(Q(seller=obj.user) & Q(check=True))
        count = reviews.count()
        return count

    def user_review_mean(self, obj):
        reviews = Review.objects.filter(Q(seller=obj.user))
        mean = reviews.aggregate(Avg('val'))['val__avg']
        return mean

    def get_phone_international(self, obj):
        return obj.countryCallingCode + obj.phone

