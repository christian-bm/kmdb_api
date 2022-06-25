from django.shortcuts import get_object_or_404
from movies.models import Movie
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Response, status

from reviews.permissions import IsAdminOrReadOnly, IsOwnerReview

from .models import Review
from .serializers import ReviewSerializer


class ReviewView(APIView, PageNumberPagination):
    def get(self, request):
        reviews = Review.objects.all()
        result_page = self.paginate_queryset(reviews, request, view=self)
        serializer = ReviewSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class ReviewAdminView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly, IsOwnerReview]

    def delete(self, request, review_id):
        try:
            review = Review.objects.get(pk=review_id)
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Review.DoesNotExist:
            return Response(
                {"message": "review with this id does not exists"},
                status.HTTP_400_BAD_REQUEST,
            )


class ReviewDetailView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie_id=movie_id)
        result_page = self.paginate_queryset(reviews, request, view=self)
        serializer = ReviewSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, movie_id):
        try:
            Movie.objects.get(pk=movie_id)
            serializer = ReviewSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(movie_id=movie_id, critic=request.user)

            return Response(serializer.data, status.HTTP_201_CREATED)
        except Movie.DoesNotExist:
            return Response({"message": "not found movie with this id"})
