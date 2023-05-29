from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate, login, logout
from .serializers import AccountSerializer, LoginSerializer
from .models import Account
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class RegisterAPIView(APIView):
    @swagger_auto_schema(
        tags=["account"],
        request_body=AccountSerializer,
        responses={
            201: openapi.Response(description="Created"),
            400: openapi.Response(description="Bad Request"),
        },
    )
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
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    @swagger_auto_schema(
        tags=["account"],
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(description="OK"),
            400: openapi.Response(description="Bad Request"),
            401: openapi.Response(description="Unauthorized"),
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    @swagger_auto_schema(tags=["account"])
    def post(self, request):
        logout(request)
        return Response({"message": "登出成功"}, status=status.HTTP_200_OK)
