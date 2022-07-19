from rest_framework import serializers, status, generics, permissions, request
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from user.models import User
from labels.models import Labels
import logging
from rest_framework.views import APIView
from labels.serializers import LabelSerializer

logger = logging.getLogger('django')


def get_user(token):
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    new_token = str(token).split("Bearer ")[1]
    encoded_token = jwt_decode_handler(new_token)
    name = encoded_token['name']
    user = User.objects.get(name=name)
    return user.id


class LabelAPIView(generics.GenericAPIView):
    serializer_class = LabelSerializer
    queryset = Labels.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            data = Labels.objects.all()
            serializer = LabelSerializer(data, many=True)
            serialized_data = serializer.data
            return Response({'status': True,
                             'message': 'Labels successfully Retrieve',
                             'data': serialized_data,
                             }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False,
                             'message': 'Something went wrong',
                             'data': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        user = request.user
        try:
            serializer = LabelSerializer(data=request.data, partial=True)
            serializer.is_valid()
            serializer.save(user_id=user.id)
            data = serializer.data
            return Response({'success': True,
                             'message': "Label created successfully",
                             'data': data
                             }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({'success': False,
                             'message': "Validation Error",
                             'data': str(e)
                             }, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'success': False,
                             'message': "Something Went wrong",
                             'data': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            data = Labels.objects.get(pk=pk)
            data.delete()
            return Response({'success': True,
                             'message': 'Successfully Deleted Data',
                             }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success': False,
                             'message': 'Something went wrong',
                             'data': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)

