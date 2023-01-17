from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from user.api.serializers import UserRegisterSerializer, UserSerializer
from user.models import User


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
    def register(self, request):
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
            }
        )
