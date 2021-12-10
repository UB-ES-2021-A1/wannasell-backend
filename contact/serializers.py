from rest_framework import serializers

from contact.models import Contact
from products.serializers import ProductDataSerializer
from profiles.models import Profile


class ContactSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    first_name = serializers.CharField(max_length=500)
    email = serializers.EmailField()
    phone = serializers.SerializerMethodField('get_phone')

    def get_phone(self, obj):
        profile = Profile.objects.get(user=obj)
        number = profile.phone
        return number


class ContactDataSerializer(serializers.ModelSerializer):
    product = ProductDataSerializer()
    buyer = ContactSerializer()
    seller = ContactSerializer()

    class Meta:
        model = Contact
        fields = ['buyer', 'seller', 'product']
