from django.contrib import admin

# Register your models here.
from favorites.models import Favorites

admin.site.register(Favorites)