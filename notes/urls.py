from django.urls import path
from notes.views import CreateAPIView, UpdateNotesAPIView, ArchiveNotesAPIView, TrashNotesAPIView, PinNotesAPIView, \
    RestoreTrashNotesAPIView

urlpatterns = [
    path('create_notes/', CreateAPIView.as_view(), name="Create_note"),
    path('get_notes/', CreateAPIView.as_view(), name="get_note"),
    path('delete_notes/<pk>/', CreateAPIView.as_view(), name="delete_note"),
    path('update_notes/<pk>/', UpdateNotesAPIView.as_view(), name="Update_notes"),
    path('archive_notes/<pk>', ArchiveNotesAPIView.as_view(), name="archive_notes"),
    path('trash_notes/<pk>', TrashNotesAPIView.as_view(), name="Trash_Notes"),
    path('get_trash_notes/', TrashNotesAPIView.as_view(), name="Get_Trash_Notes"),
    path('remove_trash_notes/<pk>', RestoreTrashNotesAPIView.as_view(), name="Trash_Notes"),
    path('pin_notes/<pk>', PinNotesAPIView.as_view(), name="pin_notes"),
    path('get/pin_notes/', PinNotesAPIView.as_view(), name="Get_pin_notes"),

]
