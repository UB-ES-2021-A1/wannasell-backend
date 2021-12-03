from rest_framework import serializers

from reviews.models import Review


class ReviewDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'seller', 'message', 'val', 'check', 'created_at']
