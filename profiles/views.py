from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, status
from profiles.models import Profile
from django.core import serializers

# Create your views here.
class ProfileView(APIView):

    def get(self, request, username, format=None):
        user_found = User.objects.filter(name__trigram_similar=username)
        serialized_profile = serializers.serialize('json', [user_found])

        return Response(serialized_profile)
