from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate, login, logout
from .serializers import AccountSerializer
from .models import Account


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()
            # 註冊成功後，已以登入的身分進行後續操作
            username = request.data.get("username")
            password = request.data.get("password")
            user = authenticate(request, username=username, password=password)
            login(request, user)
            access_token = AccessToken.for_user(user)
            token = str(access_token)
            return Response(
                {"message": "註冊成功", "username": username, "token": token},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            access_token = AccessToken.for_user(user)
            token = str(access_token)
            return Response(
                {"message": "登入成功", "username": username, "token": token},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "使用者名稱或密碼錯誤"}, status=status.HTTP_401_UNAUTHORIZED
            )

class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "登出成功"}, status=status.HTTP_200_OK)
