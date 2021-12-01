from rest_framework import serializers

from contact.models import Contact
from products.serializers import ProductDataSerializer


class ContactDataSerializer(serializers.ModelSerializer):
    product = ProductDataSerializer()

    class Meta:
        model = Contact
        fields = ['buyer', 'seller', 'product']
