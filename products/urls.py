from django.urls import path
from products.views import ProductsView

# URLConf
urlpatterns = [
    path('hello/', ProductsView.as_view())
]
