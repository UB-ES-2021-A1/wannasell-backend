from django.urls import path

from contact.views import ContactView

# URLConf
urlpatterns = [
    path('', ContactView.as_view()),
]
