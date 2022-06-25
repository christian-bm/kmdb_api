from django.db import models


class RecomendationChoices(models.TextChoices):
    MW = ("MW", "Must Watch")
    SW = ("SW", "Should Watch")
    AW = ("AW", "Avoid Watch")
    DEFAULT = ("NO", "No Opinion")


class StarsChoices(models.TextChoices):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
