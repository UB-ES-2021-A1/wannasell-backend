from django.conf.urls import url
from django.urls import path
from reviews.views import ReviewsView, MyReviewsView

# URLConf
urlpatterns = [
    path('', ReviewsView.as_view()),
    path('myreviews/', MyReviewsView.as_view())
]
