from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import User
from django.conf import settings
from .utils import register


BOT_ID = settings.BOT_ID
CHAT_ID = settings.CHAT_ID
TELEGRAM_API_URL = settings.TELEGRAM_API_URL


class AuthViewSet(ViewSet):
    @swagger_auto_schema(
        operation_description="Register",
        operation_summary="Register",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='confirm_password'),
            },
            required=['user', 'password', 'confirm_password']
        ),
        tags=['auth']
    )
    def register(self, request, *args, **kwargs):
        user = request.data['user']
        password = request.data['password']
        confirm_password = request.data['confirm_password']
        exist_user = User.objects.filter(username=user).first()

        if exist_user is not None:
            return Response(data={'message': 'A user with that username already exists'},
                            status=status.HTTP_400_BAD_REQUEST)

        validation_password = register(password, confirm_password)
        if validation_password.__class__ != str:
            return validation_password

        obj = User.objects.create(username=user, password=make_password(validation_password))
        obj.save()

        return Response(data={'message': 'User successfully registered'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Login",
        operation_summary="Login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user': openapi.Schema(type=openapi.TYPE_STRING, description='user'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            },
            required=['user', 'password']
        ),
        responses={
            200: openapi.Response('Login successful', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
        },
        tags=['auth']
    )
    def login(self, request, *args, **kwargs):
        request_user = request.data['user']
        password = request.data['password']
        user = User.objects.filter(username=request_user).first()
        if user is None:
            return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(password):
            return Response(data={'error': 'Password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['role'] = user.role

        return Response(data={'refresh': str(refresh_token), 'access_token': str(access_token)},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Reset password",
        operation_summary="Reset password",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description='old_password'),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='new_password'),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, description='confirm_password'),
            },
            required=['user', 'new_password', 'confirm_password']
        ),
        tags=['auth']
    )
    def reset_password(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data['old_password']
        password = request.data['new_password']
        confirm_password = request.data['confirm_password']
        exist_user = User.objects.filter(username=user).first()

        if not exist_user.is_authenticated:
            return Response(data={'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        if not exist_user.check_password(old_password):
            return Response(data={'message': 'Password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

        validation_password = register(password, confirm_password)
        if validation_password.__class__ != str:
            return validation_password

        user.password = make_password(validation_password)
        user.save()

        return Response(data={'message': 'Password successfully changed'}, status=status.HTTP_200_OK)
    #
    # @swagger_auto_schema(
    #     operation_description="Forgot password",
    #     operation_summary="Forgot password",
    #     tags=['auth']
    # )
    # def forgot_password(self, request, *args, **kwargs):
    #     user = request.user
    #     otp = generate_otp()
    #
    #     # obj = OtpSent.objects.create(user=user, otp=otp)
    #     # obj.save()
    #
    #     message = (f"Project: Online Examination\n"
    #                f"Otp_code:{otp}"
    #                )
    #
    #     response = requests.get(TELEGRAM_API_URL.format(BOT_ID, message, CHAT_ID))
    #
    #     if response.status_code != 200:
    #         return Response(data={'message': 'Failed to send message to Telegram.'},
    #                         status=status.HTTP_400_BAD_REQUEST)
    #
    #     return Response(data={'message': 'Your result sent to telegram bot'}, status=status.HTTP_200_OK)
    #
    # @swagger_auto_schema(
    #     operation_description="Verify Otp",
    #     operation_summary="Verify Otp",
    #     manual_parameters=[
    #         openapi.Parameter(
    #             'otp', type=openapi.TYPE_STRING, description='otp', in_=openapi.IN_QUERY, required=True)
    #     ],
    #     tags=['auth']
    # )
    # def verify_otp(self, request, *args, **kwargs):
    #     otp = request.data['otp']
