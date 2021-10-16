from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
# Create your views here.


class ProductsView(APIView):

    def get(self, request):
        """
        Return a list of all the products
        """
        return HttpResponse('Hello')
