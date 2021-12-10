from django.conf.urls import url
from django.urls import path
from reviews.views import ReviewsView

# URLConf
urlpatterns = [
    path('', ReviewsView.as_view())
]
