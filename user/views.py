from rest_framework.response import Response
from rest_framework import status
import logging
from rest_framework.views import APIView
from user.serializers import SendForgotPasswordResetEmailSerializer, UserChangePasswordSerializer,\
    UserLoginSerializer, UserForgotPasswordSerializer, UserProfileSerializer, UserRegistrationSerializer, \
    UserProfileVerificationSerializer, UserProfileVerificationEmailSerializer
from django.contrib.auth import authenticate
from user.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

logger = logging.getLogger('django')


def get_tokens_for_user(user):
    """
    function for creating token for user
    """
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    """
    API for performing user registration
    """
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="email"),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="name"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="password"),
            'password2': openapi.Schema(type=openapi.TYPE_STRING, description="confirm_password")
        }
    ))
    def post(self, request, format=None):
        """
        post method for registering a user
        """
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            token = get_tokens_for_user(user)
            logger.info("User successfully Registered ")
            activate_serializer = UserProfileVerificationEmailSerializer(data=request.data)
            activate_serializer.is_valid(raise_exception=True)
            logger.info("Verification email send successfully ")
            return Response({'success': True, 'message': 'Registration Successful, Please verified your Email',
                             'data': {'token': token}}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Registration Unsuccessful, Something went wrong',
                             'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileVerificationView(APIView):
    """
    API for user account verification
    """
    renderer_classes = [UserRenderer]

    def post(self, request, uid, format=None):
        """
        post method for verifying user account
        """
        try:
            serializer = UserProfileVerificationSerializer(data=request.data, context={'uid': uid})
            serializer.is_valid(raise_exception=True)
            logger.info("User Profile is Successfully verified ")
            return Response({'success': True,
                             'msg': 'User Profile is Successfully verified '}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Something Went Wrong',
                             'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    API for performing login operation
    """
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request, format=None):
        """
        post method for checking login operation
        """
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            print(user)
            if user is not None:
                token = get_tokens_for_user(user)
                logger.info("User is successfully logged in")
                return Response({'success': True, 'message': 'Login Success',
                                 'data': {'token': token}}, status=status.HTTP_200_OK)
            else:
                logger.error("Something went wrong in password or email")
                return Response({'success': False, 'message': 'Login failed!',
                                 'data': {'username': serializer.data.get('username')}},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Login failed!, Something Went Wrong',
                             'data': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """
    API for checking user details
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UserProfileSerializer)
    def get(self, request, format=None):
        """
        get function for checking user details
        """
        try:
            serializer = UserProfileSerializer(request.user)
            logger.info("User successfully access the profile")
            return Response({'success': True, 'message': 'User Profile',
                             'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Something Went Wrong',
                             'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserChangePasswordView(APIView):
    """
    API for user change password with login and token
    """
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=UserChangePasswordSerializer)
    def post(self, request, format=None):
        """
        function for change user password
        """
        try:
            serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
            serializer.is_valid(raise_exception=True)
            logger.info("User successfully changed the password")
            return Response({'success': True, 'msg': 'Password Changed Successfully',
                             'data': serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': 'Something Went Wrong',
                             'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SendForgotPasswordResetEmailView(APIView):
    """
    API for sending reset mail for forgot password
    """
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="email")
        }
    ))
    def post(self, request, format=None):
        """
        function for sending mail for reset password
        """
        try:
            serializer = SendForgotPasswordResetEmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            logger.info("Reset email is successfully sent")
            return Response({'success': True,
                             'msg': 'Password Reset link send. Please check your Email',
                             'data': serializer.data},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Something Went Wrong',
                             'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserForgotPasswordResetView(APIView):
    """
    API for reset password for forget password user
    """
    renderer_classes = [UserRenderer]

    @swagger_auto_schema(request_body=UserForgotPasswordSerializer)
    def post(self, request, uid, token, format=None):
        """
        function for changing user password
        """
        try:
            serializer = UserForgotPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
            serializer.is_valid(raise_exception=True)
            logger.info("Forgot password is successfully reset")
            return Response({'success': True,
                             'msg': 'Password Reset Successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False, 'message': 'Something Went Wrong',
                             'data': str(e)}, status=status.HTTP_400_BAD_REQUEST)









