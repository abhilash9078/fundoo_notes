from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import status, generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from user.models import User
from notes.models import Notes
import logging
from django.core.cache import cache
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from notes.serializers import NotesSerializer, PinSerializer, TrashSerializer
from fundoo_notes import settings

logger = logging.getLogger('django')
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def get_user(token):
    """
    function for checking and verifying token for valid user
    """
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
    new_token = str(token).split("Bearer ")[1]
    encoded_token = jwt_decode_handler(new_token)
    name = encoded_token['name']
    user = User.objects.get(name=name)
    return user.id


class CreateAPIView(generics.GenericAPIView):
    """
    API for creating Notes and performing all CRUD operation
    """
    serializer_class = NotesSerializer
    queryset = Notes.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, "token", type=openapi.TYPE_STRING)
    ])
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        """
        function for getting all the notes of that user
        """
        user_id = request.user.id
        username = request.user.name
        try:
            cache_key = str(user_id)
            note = Notes.objects.filter(user=request.user, is_trash=False,
                                        is_archive=False).order_by('-is_pinned')
            serializer = NotesSerializer(note, many=True)
            logger.info('Getting the notes data on %s', timezone.now())
            serialized_data = serializer.data
            c_data = cache.get(cache_key)

            logger.info("User successfully retrieve the data")
            return Response({'success': True,
                             'message': "Successfully retrieve the notes",
                             'data': serialized_data, 'Data_recent': c_data}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': "Something went Wrong, User is not exists",
                             'data': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('TOKEN', openapi.IN_HEADER, "token", type=openapi.TYPE_STRING)
    ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description")
            }
        ))
    def post(self, request):
        """
        function for creating notes for a particular user
        """
        user = request.user
        label = request.data['label']
        user_id = request.user.id

        try:
            cache_key = str(user_id)
            serializer = NotesSerializer(data=request.data, partial=True)
            serializer.is_valid()
            serializer.save(user_id=user.id)
            data = serializer.data
            cache.set(cache_key, data)
            logger.info("Notes created successfully")
            return Response({'success': True,
                             'message': "Notes Create Successfully",
                             'data': data
                             }, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            logger.error(e)
            return Response({'success': False,
                             'message': f"Some Validation error is happened{e}",
                             }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': "Something went wrong",
                             'data': str(e)}, status=status.HTTP_417_EXPECTATION_FAILED)

    def delete(self, request, pk):
        """
        function for deleting note
        """
        try:
            cache_key = str(pk)
            data = Notes.objects.get(pk=pk)
            data.delete()
            cache.delete(cache_key)
            logger.info("Notes deleted successfully")
            return Response({'success': True,
                             'message': "Notes deleted successfully",
                             }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({
                'success': False,
                'message': "Something went wrong, User is not exists",
            }, status=status.HTTP_404_NOT_FOUND)


class UpdateNotesAPIView(generics.GenericAPIView):
    """
    API for updating notes
    """
    serializer_class = NotesSerializer
    data = Notes.objects.all()

    def get_objects(self, pk):
        """
        function for get the note id for updating
        """
        try:
            return Notes.objects.get(pk=pk)
        except Exception as e:
            return Response({'success': False,
                             'message': f"Something Went Wrong {e}",
                             }, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        function for checking user details for update
        """
        pk = self.kwargs.get('pk')
        cache_key = str(pk)
        note = self.get_objects(pk=pk)
        serializer = NotesSerializer(note)
        cache.update(cache_key, serializer)
        logger.info("Successfully got the notes for update ")
        return Response({'success': True,
                         'message': "Successfully got the notes",
                         'data': serializer.data
                         }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """
        function for updating notes for valid user
        """
        pk = self.kwargs.get('pk')
        note = self.get_objects(pk=pk)
        serializer = NotesSerializer(note, data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                note = Notes.objects.get(pk=pk)
                if note.is_archive:
                    note.is_pinned = False
                    note.save()
                logger.info("Successfully updated the notes")
                return Response({'success': True,
                                 'message': "Successfully updated the notes",
                                 'data': serializer.data
                                 }, status=status.HTTP_200_OK)
            return Response({'success': False,
                             'message': "Something went wrong",
                             }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': "Something went wrong",
                             }, status=status.HTTP_400_BAD_REQUEST)


class ArchiveNotesAPIView(generics.GenericAPIView):
    """
    API for make notes Archive
    """
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'note_id': openapi.Schema(type=openapi.TYPE_STRING, description="note id")
        }
    ))
    def put(self, request, *args, **kwar):
        """
        function for making notes to archive notes
        """
        pk = self.kwargs.get('pk')
        note_id = pk
        note = Notes.objects.get(id=note_id)
        try:
            if not note.is_archive:
                note.is_archive = True
                note.save()
                logger.info("Notes is moved to Trash ")
                return Response({'success': True,
                                 'message': 'Notes is archive successfully'
                                 }, status=status.HTTP_200_OK)
            elif note.is_archive:
                note.is_archive = False
                note.save()
                logger.info("Notes is removed from archive")
                return Response({'success': True,
                                 'message': 'Notes is Moved from archive successfully'
                                 }, status=status.HTTP_200_OK)

        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': 'Oops! Something went wrong! Please try again...',
                             'Data': str(e),
                             }, status=status.HTTP_400_BAD_REQUEST)


class TrashNotesAPIView(generics.GenericAPIView):
    """
    API for moving notes to trash
    """
    serializer_class = TrashSerializer
    queryset = Notes.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        function for getting all trash notes
        """
        try:
            trash = Notes.objects.filter(user=request.user, is_trash=True)
            serializer = TrashSerializer(trash, many=True)
            serializer_data = serializer.data
            return Response({"success": True,
                             "msg": "Getting all the Trash notes Successfully",
                             "data": serializer_data
                             }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False,
                             "msg": "Something went wrong",
                             "data": str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'note_id': openapi.Schema(type=openapi.TYPE_STRING, description="note id")
        }
    ))
    def put(self, request, *args, **kwar):
        """
        function for making notes to trash notes
        """
        pk = self.kwargs.get('pk')
        note_id = pk
        note = Notes.objects.get(id=note_id)
        try:
            if not note.is_trash:
                note.is_trash = True
                note.save()
                logger.info("Notes is moved to Trash ")
                return Response({'success': True,
                                 'message': 'Notes is set in Trash successfully'
                                 }, status=status.HTTP_200_OK)
            elif note.is_trash:
                logger.info("Notes is already in trash")
                return Response({'success': True,
                                 'message': 'Notes is already in Trash'
                                 }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': 'Something went wrong, Please try again...',
                             'data': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)


class RestoreTrashNotesAPIView(generics.GenericAPIView):
    """
    API for restoring notes from trash
    """
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'note_id': openapi.Schema(type=openapi.TYPE_STRING, description="note id")
        }
    ))
    def put(self, request, *args, **kwar):
        """
        function to restore corresponding trash note
        """
        pk = self.kwargs.get('pk')
        note_id = pk
        note = Notes.objects.get(id=note_id)
        try:
            if note.is_trash:
                note.is_trash = False
                note.save()
                logger.info("Notes is Restore from Trash")
                return Response({'success': True,
                                 'message': 'Notes is Removed from Trash successfully'
                                 }, status=status.HTTP_200_OK)
            else:
                logger.info("Notes is not in Trash")
                return Response({'success': False,
                                 'message': 'Notes is not in Trash!'
                                 }, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': 'Something went wrong, Please try again...',
                             'data': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)


class PinNotesAPIView(generics.GenericAPIView):
    """
    API for pin a note
    """
    serializer_class = PinSerializer
    queryset = Notes.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        function for getting all the notes
        """
        try:
            pin = Notes.objects.filter(user=request.user, is_pinned=True)
            serializer = PinSerializer(pin, many=True)
            return Response({"success": True,
                             "msg": 'Retrieve all pinned notes',
                             "data": serializer.data
                             }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False,
                             "msg": "Something went wrong",
                             "data": str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'note_id': openapi.Schema(type=openapi.TYPE_STRING, description="note id")
        }
    ))
    def put(self, request, *args, **kwar):
        """
        function for pin a note 
        """
        pk = self.kwargs.get('pk')
        note_id = pk
        note = Notes.objects.get(id=note_id)
        try:
            if not note.is_pinned:
                note.is_pinned = True
                note.save()
                logger.info("Notes is pinned successfully")
                return Response({'success': True,
                                 'message': 'Notes is pinned Successfully'
                                 }, status=status.HTTP_200_OK)
            elif note.is_pinned:
                note.is_pinned = False
                note.save()
                logger.info("Notes is unpinned successfully")
                return Response({'success': True,
                                 'message': 'Notes is unpinned Successfully'
                                 }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.exception(e)
            return Response({'success': False,
                             'message': 'Something went wrong, Please try again...',
                             'data': str(e)
                             }, status=status.HTTP_400_BAD_REQUEST)
