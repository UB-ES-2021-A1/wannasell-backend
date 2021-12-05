"""wannasellbackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import confirm_email
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth api urls
    url(r'^api/v1/auth/', include('rest_auth.urls')),
    url(r'^api/v1/auth/register/', include('rest_auth.registration.urls')),
    url(r'^api/v1/auth/register/confirm/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    url(r'^api/v1/accounts/', include('django.contrib.auth.urls')),
    url(r'^api/v1/profile/', include('profiles.urls')),
    path('api/v1/favorites/', include('favorites.urls')),
    path('api/v1/products/', include('products.urls')),
    url(r'^api/v1/contact/', include('contact.urls')),
    url(r'^api/v1/reviews/', include('reviews.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
