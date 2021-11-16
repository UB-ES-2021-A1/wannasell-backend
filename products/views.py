import ntpath
import operator
from functools import reduce

from django.core.files import File
from django.db.models import QuerySet, Q
from django.db.models.sql import AND

from .forms import ImageForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import products.models
from products.serializers import ProductDataSerializer, CategoryDataSerializer, ImageDataSerializer

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

from products.models import Product, Category, Image


# Create your views here.

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ProductsView(APIView):
    serializer_class = ProductDataSerializer

    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        """
        Return a list of all the products
        """
        try:
            category = request.GET.get('category')
            id = request.GET.get('id')
            search = request.GET.get('search')
            seller = request.GET.get('seller')
            qs = []

            if category is not None:
                qs.append(Q(category__name=category))
            if search is not None:
                qs.append(Q(title__icontains=search))
            if id is not None:
                qs.append(Q(id=id))
            if seller is not None:
                qs.append(Q(seller__username=seller))

            products = Product.objects.filter(reduce(operator.and_, qs)) if len(qs) > 0 else Product.objects.all()

            products_serialized = [ProductDataSerializer(prod).data for prod in products]
            response_status = status.HTTP_200_OK if products else status.HTTP_204_NO_CONTENT
            return Response(products_serialized, status=response_status)
        except Exception as e:
            print(e)
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


class ProductIdView(APIView):
    """
        Reads Profile fields
        Accepts GET method.

        Default display fields: id, avatar, bio, address

        Returns Profile fields.
    """

    serializer_class = ProductDataSerializer

    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, id=None):
        try:
            product = Product.objects.get(id=id)
        except products.models.Product.DoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if product:
            serialized_profile = ProductDataSerializer(instance=product)
            return Response(serialized_profile.data, status=status.HTTP_200_OK)


class CategoriesView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        """
        Return a list of all the categories
        """
        categories = Category.objects.all()
        categories_serialized = [CategoryDataSerializer(cat).data for cat in categories]
        response_status = status.HTTP_200_OK if categories else status.HTTP_204_NO_CONTENT
        return Response(categories_serialized, status=response_status)


class ImagesView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):
        """
        Return a list of the images of a product
        """
        try:
            product = Product.objects.get(id=request.GET.get('id'))
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        images = Image.objects.filter(product=product)
        images_serialized = [ImageDataSerializer(im).data for im in images]
        response_status = status.HTTP_200_OK if images else status.HTTP_204_NO_CONTENT
        return Response(images_serialized, status=response_status)

    def post(self, request):
        """
        Post images for a certain product
        """

        prod_id = request.GET.get('id')
        images = request.FILES.getlist('image')
        if len(images) == 0 or not prod_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                product_image = form.save(commit=False)
                product_image.product = Product.objects.get(id=prod_id)
                product_image.save()
        except:
            return Response(status=status.HTTP_418_IM_A_TEAPOT)

        return Response(status=status.HTTP_201_CREATED)
