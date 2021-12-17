from django.contrib import admin
# Register your models here.
from reviews.models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'seller', 'check', 'created_at',)
    list_filter = ('check',)
admin.site.register(Review, ReviewAdmin)