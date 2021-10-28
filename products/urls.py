from django.urls import path
from products.views import ProductsView, CategoriesView, ImagesView

# URLConf
urlpatterns = [
    path('', ProductsView.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('images/', ImagesView.as_view())
]
