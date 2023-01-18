from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from user.api.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    UserLoginSerializer,
)
from user.models import User
from utils import error_messages


class AuthViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[AllowAny],
        url_path="register",
    )
    def register(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = self.serializer_class(instance=user).data
        refresh = RefreshToken.for_user(user)
        token_dict = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "expires_at": refresh.access_token["exp"],
        }

        return Response(
            {
                "token": token_dict,
                "user": user_data,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[AllowAny],
        url_path="login",
    )
    def login(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)
        token_dict = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "expires_at": refresh.access_token["exp"],
        }
        user_data = self.serializer_class(instance=user).data

        return Response(
            {
                "token": token_dict,
                "user": user_data,
            }
        )

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
        url_path="logout",
    )
    def logout(self, request):
        try:
            token = RefreshToken(request.data.get("refresh"))
            token.blacklist()
        except TokenError:
            raise ValidationError(
                error_messages.AUTH_LOGOUT_FAILED, code="AUTH_LOGOUT_FAILED"
            )

        return Response(
            {
                "result": True,
            }
        )
