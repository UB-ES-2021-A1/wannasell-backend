from django.conf.urls import url

from profiles.views import ProfileView, ProfileIdView

urlpatterns = [
    # URLs that do not require a session or valid token
    url(r'^$', ProfileView.as_view()),
    url(r'^(?P<id>\d+)/$', ProfileIdView.as_view()),
]