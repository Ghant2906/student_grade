from rest_framework import serializers
from .models import Users, Classes, Courses, Grades
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

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'

class ClassesSeriralizer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    class Meta:
        model = Classes
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    course = CourseSerializer(source='enrollment.class_field.course', read_only=True)
    class Meta:
        model = Grades
        fields = ['course', 'midterm', 'final', 'additional_grade_1', 'additional_grade_2', 'additional_grade_3']
