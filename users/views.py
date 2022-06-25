from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView, Response, status

from .models import User
from .permissions import IsAdminOrReadOnly
from .serializers import UserLoginSerializer, UserSerializer


class UserView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        users = User.objects.all()
        result_page = self.paginate_queryset(users, request, view=self)
        serializer = UserSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class UserDetailView(APIView, PageNumberPagination):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "invalid email or password"}, status.HTTP_401_UNAUTHORIZED
            )

        token, created = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})
