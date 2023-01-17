from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.exceptions import ValidationError

from utils import error_messages

User = get_user_model()


class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(label="email", required=True)
    password = serializers.CharField(
        write_only=True,
        style={"input_type": "password", "placeholder": "password"},
        validators=[validate_password],
    )

    def validate(self, attrs):
        user = User.objects.filter(email=attrs.get("email")).first()

        if user:
            raise ValidationError(
                error_messages.USER_EMAIL_DUPLICATED, code="USER_EMAIL_DUPLICATED"
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "created_at", "updated_at"]
