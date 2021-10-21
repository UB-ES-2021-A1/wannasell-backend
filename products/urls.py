from django.urls import path
from products.views import ProductsView, CategoriesView

# URLConf
urlpatterns = [
    path('', ProductsView.as_view()),
    path('categories/', CategoriesView.as_view())
]
