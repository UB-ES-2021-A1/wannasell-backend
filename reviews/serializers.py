from rest_framework import serializers

from profiles.models import Profile
from profiles.serializers import UserSerializer
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


class ReviewReturnDataSerializer(serializers.Serializer):
    seller = UserSerializer()
    reviewer = UserSerializer()
    message = serializers.CharField(max_length=500, allow_blank=True)
    val = serializers.IntegerField()
    created_at = serializers.DateTimeField(format="%d-%b-%Y", read_only=True)
    reviewer_avatar = serializers.SerializerMethodField("get_avatar")

    def get_avatar(self, obj):
        reviewer = Profile.objects.get(user__username=obj.reviewer.username)
        return reviewer.avatar.url
