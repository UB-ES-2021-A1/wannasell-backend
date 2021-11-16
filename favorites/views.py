from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import products.models
from products.serializers import ProductDataSerializer

from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS

from favorites.models import Favorites
from favorites.serializers import FavDataSerializer
from products.models import Product
from django.contrib.auth.models import User


# Create your views here.
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class FavoritesView(APIView):
    # serializer_class = ProductDataSerializer

    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def post(self, request, id=None):
        if id:
            try:
                prod = Product.objects.get(id=id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            try:
                Favorites.objects.create(user=request.user, product=prod)
            except:
                return Response('Already exists', status=status.HTTP_418_IM_A_TEAPOT)

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None):
        if id:
            try:
                prod = Product.objects.get(id=id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)

            try:
                fav = Favorites.objects.filter(user=request.user, product=prod).delete()
            except:
                return Response('Not found', status=status.HTTP_404_NOT_FOUND)

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)