from rest_framework.views import APIView
from myapp.models import Users
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime

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
    