from django.urls import path
from reviews.views import ReviewDetailView

from . import views

urlpatterns = [
    path("movies/", views.MovieView.as_view()),
    path("movies/<int:movie_id>", views.MovieDetailView.as_view()),
    path("movies/<int:movie_id>/reviews/", ReviewDetailView.as_view()),
]
