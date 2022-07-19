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

logger = logging.getLogger('django')


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
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
    renderer_classes = [UserRenderer]

    def post(self, request, uid, format=None):
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
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
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
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
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
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
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
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
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
    renderer_classes = [UserRenderer]

    def post(self, request, uid, token, format=None):
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









