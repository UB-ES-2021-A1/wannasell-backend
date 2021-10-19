from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from products.serializers import ProductDataSerializer, CategoryDataSerializer
import json

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from products.models import Product, Category

# Create your views here.


class ProductsView(APIView):

    serializer_class = ProductDataSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        """
        Return a list of all the products
        """
        category = request.GET.get('category')
        if category:
            cat = Category.objects.get(name=category)
            products = list(Product.objects.filter(category=cat))
            products_serialized = [ProductDataSerializer(prod).data for prod in products]
            response_status = status.HTTP_200_OK if products else status.HTTP_204_NO_CONTENT
            return Response(products_serialized, status=response_status)

        products = list(Product.objects.all())
        products_serialized = [ProductDataSerializer(prod).data for prod in products]
        response_status = status.HTTP_200_OK if products else status.HTTP_204_NO_CONTENT
        return Response(products_serialized, status=response_status)


class CategoriesView(APIView):

    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        """
        Return a list of all the categories
        """
        categories = Category.objects.all()
        categories_serialized = [CategoryDataSerializer(cat).data for cat in categories]
        response_status = status.HTTP_200_OK if categories else status.HTTP_204_NO_CONTENT
        return Response(categories_serialized, status=response_status)