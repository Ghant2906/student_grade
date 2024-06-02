from rest_framework.views import APIView
from myapp.models import Users
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response

class GetAllUsersAPIView(APIView):
    def get(self, request):
        users = Users.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)