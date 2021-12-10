import operator
from functools import reduce

from django.contrib.auth.models import User
import django.contrib.auth.models as mods
from django.db.models import Q
from rest_framework import status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView

import reviews.models
from reviews.models import Review
from reviews.serializers import ReviewDataSerializer, ReviewReturnDataSerializer


# Create your views here.

class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class ReviewsView(APIView):
    serializer_class = ReviewDataSerializer

    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    """
    GET: "api/v1/reviews/?seller=username" Returns the reviews done on that user
    POST: "api/v1/reviews/?seller=username" + {"message": "text", "val": n} Adds a review on that user
    PATCH: "api/v1/reviews/?seller=username1" +  {"message": "text", "val": n, "check": False} Modifies
            the review done on username1 by username2, pls set the check to False in the dict so the admin has to check the
            modification
    """

    def get(self, request):
        """
        Return a list of all the products
        """
        try:
            seller = request.GET.get('seller')
            qs = [Q(check=True)]
            if seller is not None and seller != "":
                qs.append(Q(seller__username=seller))
            else:
                return Response('Seller not provided', status=status.HTTP_400_BAD_REQUEST)

            reviews = Review.objects.filter(reduce(operator.and_, qs))

            reviews_serialized = [ReviewReturnDataSerializer(rev).data for rev in reviews]
            response_status = status.HTTP_200_OK if reviews else status.HTTP_204_NO_CONTENT
            return Response(reviews_serialized, status=response_status)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        seller = request.GET.get('seller')
        if seller is None or seller == "":
            return Response('Seller not provided', status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                s = User.objects.get(username=seller)
            except:
                return Response("Couldn't find seller", status=status.HTTP_404_NOT_FOUND)
        try:
            r = Review.objects.create(
                reviewer=request.user,
                seller=s,
                message=request.data.get('message'),
                val=request.data.get('val')
            )
            r.save()
        except:
            return Response("Couldn't create review", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'id': r.id}, status=status.HTTP_200_OK)

    def patch(self, request):
        seller = request.query_params['seller']
        b = request.user
        try:
            s = User.objects.get(username=seller)
        except:
            return Response('Buyer or Seller not found', status=status.HTTP_404_NOT_FOUND)

        try:
            rev = Review.objects.get(seller=s, reviewer=b)
        except:
            return Response('Review not found', status=status.HTTP_404_NOT_FOUND)

        serialized_review = ReviewDataSerializer(instance=rev, data=request.data, partial=True)

        if serialized_review.is_valid():
            serialized_review.save()
            return Response(serialized_review.data, status=status.HTTP_200_OK)
        return Response('Bad Request :(', status=status.HTTP_400_BAD_REQUEST)


class MyReviewsView(APIView):
    serializer_class = ReviewDataSerializer

    permission_classes = [IsAuthenticated | ReadOnly]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    """
    GET: "api/v1/reviews/myreviews/" Returns the reviews done by that user
    """

    def get(self, request):
        try:
            reviewer = request.user.username
            qs = [Q(check=True), Q(reviewer__username=reviewer)]
            reviews = Review.objects.filter(reduce(operator.and_, qs))

            reviews_serialized = [ReviewReturnDataSerializer(rev).data for rev in reviews]
            response_status = status.HTTP_200_OK if reviews else status.HTTP_204_NO_CONTENT
            return Response(reviews_serialized, status=response_status)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)