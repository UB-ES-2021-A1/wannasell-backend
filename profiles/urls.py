from django.conf.urls import url

from profiles.views import ProfileView

urlpatterns = [
    # URLs that do not require a session or valid token
    url(r'(?P<username>)/$', ProfileView.as_view()),
]