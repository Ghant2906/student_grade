from rest_framework.views import APIView
from myapp.models import Users, Classes, Enrollments, Grades
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer, ClassesSeriralizer, GradeSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.db.models import Q

class UsersAPI(APIView):
    def get(self, request):
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class LoginAPI(APIView):
    def post(self, request):
        data_login = LoginSerializer(data=request.data)
        if not data_login.is_valid():
            return Response("du lieu gui len sai roi", status=status.HTTP_400_BAD_REQUEST)
        email = data_login.data['email']
        password = data_login.data['password']
        user_info = Users.objects.filter(email=email, password=password, role_id=3).values(
            'id', 'email', 'full_name', 'avatar_url', 'created_at').first()
        if user_info is None:
            return Response("tai khoan hoac mat khau khong chinh xac", status=status.HTTP_400_BAD_REQUEST)
        
        refresh = RefreshToken.for_user(Users.objects.get(id=user_info['id']))
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_info': user_info
        }, status=status.HTTP_200_OK)
    
class RegisterAPI(APIView):
    def post(self, request):
        data_register = RegisterSerializer(data=request.data)
        if not data_register.is_valid():
            return Response("du lieu gui len sai roi", status=status.HTTP_400_BAD_REQUEST)
        email = data_register.data['email']
        password = data_register.data['password']
        full_name = data_register.data['full_name']
        avatar_url = data_register.data['avatar_url']
        student_code = data_register.data['student_code']
        user_info = Users.objects.create(email=email, password=password, full_name=full_name, avatar_url=avatar_url, studen_code=student_code, role_id=3, created_at=datetime.now(), is_active= True)
        return Response({"id": user_info.id, "message": "Đăng ký thành công"}, status=status.HTTP_200_OK)
    

class GetStudentsByClasses(APIView):
    def get (self, request, class_id):
        classes = get_object_or_404(Classes, pk=class_id)
        enrollments = Enrollments.objects.filter(class_field=classes)
        students = Users.objects.filter(id__in=enrollments.values('student_id'))
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data)
    
class GetClassByLecturer(APIView):
    def get (self, request, instructor_id):
        instructor = get_object_or_404(Users, pk=instructor_id)
        classes = Classes.objects.filter(instructor=instructor)
        serializer = ClassesSeriralizer(classes, many=True)
        return Response(serializer.data)
    
class GetStudentByCodeOrName(APIView):
    def get (self, request, student_code_or_name):
        users = Users.objects.filter(
            (Q(studen_code=student_code_or_name) | Q(full_name=student_code_or_name)) & Q(role_id=3)
        )
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class GetCourseAndGradeByStudent(APIView):
    def get (self, request, student_id):
        student = get_object_or_404(Users, pk=student_id)
        gradeOfStudent = Grades.objects.filter(enrollment__student=student)
        serializer = GradeSerializer(gradeOfStudent, many=True)
        return Response(serializer.data)