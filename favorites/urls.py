from django.conf.urls import url
from django.urls import path
from favorites.views import FavoritesView, FavoritesByUserView

# URLConf
urlpatterns = [
    path('', FavoritesView.as_view()),
    url(r'^(?P<id>\d+)/$', FavoritesView.as_view())
]
