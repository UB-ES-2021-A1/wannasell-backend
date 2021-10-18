from rest_auth.serializers import serializers

from utils.serializers import Base64ImageField


class ProfileDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    avatar = serializers.ImageField(allow_null=False)
    bio = serializers.CharField(max_length=500, allow_blank=True)
    address = serializers.CharField(max_length=1024, allow_blank=True)

    def update(self, instance, validated_data):
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance
