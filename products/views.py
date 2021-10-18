from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class ProductsView(APIView):

    def get(self, request):
        """
        Return a list of all the products
        """
        pass
