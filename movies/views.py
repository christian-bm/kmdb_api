from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Response, status

from .models import Movie
from .permissions import IsAdminOrReadOnly
from .serializers import MovieSerializer


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def patch(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            serializer = MovieSerializer(movie, request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found."}, status.HTTP_404_NOT_FOUND)

    def delete(self, request, movie_id):
        try:
            movie = Movie.objects.get(pk=movie_id)
            movie.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Movie.DoesNotExist:
            return Response({"message": "Movie not found."}, status.HTTP_404_NOT_FOUND)
