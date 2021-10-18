from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class ProductsView(APIView):

    def get(self, request):
        """
        Return a list of all the products
        """
        pass


class CategoriesView(APIView):

    def get(self, request):
        """
        Return a list of all the categories
        """
        pass


class CategoryProductsView(APIView):

    def get(self, request):
        """
        Given a category, return the products that belong to that category
        """
        pass
