from django.urls import path

from . import views

urlpatterns = [
    path("reviews/", views.ReviewView.as_view()),
    path("reviews/<int:review_id>", views.ReviewAdminView.as_view()),
]
