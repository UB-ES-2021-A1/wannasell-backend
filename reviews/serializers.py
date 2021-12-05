from rest_framework import serializers

from reviews.models import Review


class ReviewDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'seller', 'message', 'val', 'check', 'created_at']

    def update(self, instance, validated_data):
        instance.reviewer = validated_data.get('reviewer', instance.reviewer)
        instance.seller = validated_data.get('seller', instance.seller)
        instance.message = validated_data.get('message', instance.message)
        instance.val = validated_data.get('val', instance.val)
        instance.check = validated_data.get('check', instance.check)
        instance.save()
        return instance