from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.serializers import ProductDataSerializer, CategoryDataSerializer

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

from products.models import Product, Category
from profiles.models import User


# Create your views here.

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ProductsView(APIView):
    serializer_class = ProductDataSerializer

    permission_classes = [IsAuthenticated|ReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        """
        Return a list of all the products
        """
        try:
            category = request.GET.get('category')
            id = request.GET.get('id')

            if category:
                cat = Category.objects.get(name=category)
                products = list(Product.objects.filter(category=cat))
            elif id:
                products = Product.objects.filter(id=id)
            else:
                products = list(Product.objects.all())

            products_serialized = [ProductDataSerializer(prod).data for prod in products]
            response_status = status.HTTP_200_OK if products else status.HTTP_204_NO_CONTENT
            return Response(products_serialized, status=response_status)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            category = Category.objects.get(name=request.POST.get('category_name'))

            Product.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                price=request.POST.get('price'),
                seller=request.user,
                category=category
            )
        except:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)
        return Response(status=status.HTTP_200_OK)

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
