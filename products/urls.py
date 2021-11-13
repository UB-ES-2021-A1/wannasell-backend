from django.conf.urls import url
from django.urls import path
from products.views import ProductsView, CategoriesView, ImagesView, ProductIdView

# URLConf
urlpatterns = [
    path('', ProductsView.as_view()),
    url(r'^(?P<id>\d+)/$', ProductIdView.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('images/', ImagesView.as_view())
]
