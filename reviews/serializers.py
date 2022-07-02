from rest_framework import serializers
from users.serializers import UserReviewSerializer

from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    movie_id = serializers.IntegerField(read_only=True)
    critic = UserReviewSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "stars",
            "review",
            "spoilers",
            "recomendation",
            "movie_id",
            "critic",
        ]
        depth = 0

        read_only_fields = ["id", "critic"]

    def create(self, validated_data: dict):
        return Review.objects.create(**validated_data)
