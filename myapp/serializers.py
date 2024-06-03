from rest_framework import serializers
from .models import Users
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


def validate_email_domain(value):
    if not value.endswith('@donga.vn'):
        raise ValidationError("Email phải có đuôi '@donga.vn'.")

class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, validators=[validate_email_domain])
    password = serializers.CharField(max_length=255)
    full_name = serializers.CharField(max_length=255)
    avatar_url = serializers.CharField(max_length=255)
    student_code = serializers.CharField(max_length=255)
