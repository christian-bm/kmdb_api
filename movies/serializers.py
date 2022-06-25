from os import name

from genres.models import Genre
from genres.serializers import GenreSerializer
from rest_framework import serializers

from .models import Movie


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127)
    premiere = serializers.DateField()
    duration = serializers.CharField(max_length=10)
    classification = serializers.IntegerField()
    synopsis = serializers.CharField()

    genres = GenreSerializer(many=True)

    def create(self, validated_data: dict):
        genres = validated_data.pop("genres")

        genres_in_db = []
        for genre in genres:
            try:
                db_genre = Genre.objects.get(name=genre["name"])
                genres_in_db.append(db_genre)
            except Genre.DoesNotExist:
                db_genre = Genre.objects.create(**genre)
                genres_in_db.append(db_genre)

        movie = Movie.objects.create(**validated_data)
        movie.genres.set(genres_in_db)

        return movie

    def update(self, instance: Movie, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
