from django.db import models

from .utils import RecomendationChoices, StarsChoices


class Review(models.Model):
    stars = models.IntegerField(choices=StarsChoices.choices)
    review = models.TextField()
    spoilers = models.BooleanField()
    recomendation = models.CharField(
        max_length=50,
        choices=RecomendationChoices.choices,
        default=RecomendationChoices.DEFAULT,
    )

    critic = models.ForeignKey("users.User", on_delete=models.CASCADE)
    movie = models.ForeignKey("movies.Movie", on_delete=models.CASCADE)
