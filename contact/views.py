from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from contact.models import Contact
from contact.serializers import ContactDataSerializer
from products.models import Product


class ContactView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        user = request.user
        user_contacts = Contact.objects.filter(Q(buyer=user) | Q(seller=user))
        contacts_serialized = [ContactDataSerializer(contact).data for contact in user_contacts]
        response_status = status.HTTP_200_OK if contacts_serialized else status.HTTP_204_NO_CONTENT
        return Response(contacts_serialized, status=response_status)

    def post(self, request):
        buyer = request.user

        try:
            seller_username = request.data.get('seller')
            seller = User.objects.get(username=seller_username)
            product_id = request.data.get('product_id')
            product = Product.objects.get(id=product_id)
            contact = Contact.objects.create(
                buyer=buyer,
                seller=seller,
                product=product
            )
            contact.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(ContactDataSerializer(contact).data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        user = request.user
        product_id = request.data.get('product_id')

        try:
            product = Product.objects.get(id=product_id)
            contact = Contact.objects.filter(Q(buyer=user) & Q(product=product))
            contact.delete()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_201_CREATED)




