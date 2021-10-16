from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import profiles
from profiles.models import Profile
from profiles.serializers import ProfileDetailsSerializer


class ProfileView(APIView):
    """
        Reads and updates Profile fields
        Accepts GET, PUT, PATCH methods.

        Default accepted fields: avatar, bio, address
        Default display fields: id, avatar, bio, address
        Read-only fields: id

        Returns Profile fields.
    """

    serializer_class = ProfileDetailsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request):

        username = request.GET.get('username')

        if not username:
            profile = Profile.objects.get(user=self.request.user)
            serializer = ProfileDetailsSerializer(profile)
            return Response(serializer.data, status.HTTP_200_OK)

        try:
            user = User.objects.get(username=username)
            profile = Profile.objects.get(user=user)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            serializer = ProfileDetailsSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        username = request.GET.get('username')

        # If username provided by parameters
        if username:
            # If request user has perms to modify others profiles
            if request.user.has_perm('profiles.modify_other_profiles'):
                try:
                    # Define the profile to be modified as the given by parameters
                    user = User.objects.get(username=username)
                    profile = Profile.objects.get(user=user)
                except:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            # If no username provided we use requester user as default
            profile = Profile.objects.get(user=self.request.user)

        serializer = ProfileDetailsSerializer(instance=profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        username = request.GET.get('username')

        # If username provided by parameters
        if username:
            # If request user has perms to modify others profiles
            if request.user.has_perm('profiles.modify_other_profiles'):
                try:
                    # Define the profile to be modified as the given by parameters
                    user = User.objects.get(username=username)
                    profile = Profile.objects.get(user=user)
                except:
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        profile = Profile.objects.get(user=self.request.user)

        serializer = ProfileDetailsSerializer(instance=profile, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileIdView(APIView):
    """
        Reads Profile fields
        Accepts GET method.

        Default display fields: id, avatar, bio, address

        Returns Profile fields.
    """

    serializer_class = ProfileDetailsSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def get(self, request, id=None):
        try:
            profile = Profile.objects.get(id=id)
        except profiles.models.Profile.DoesNotExist:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if profile:
            serialized_profile = ProfileDetailsSerializer(instance=profile)
            return Response(serialized_profile.data, status=status.HTTP_200_OK)
