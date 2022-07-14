from django.urls import path
from notes.views import CreateAPIView, UpdateNotesAPIView, ArchiveNotesAPIView, TrashNotesAPIView, PinNotesAPIView, \
    RemoveTrashNotesAPIView, LabelAPIView

urlpatterns = [
    path('create_notes/', CreateAPIView.as_view(), name="Create_note"),
    path('get_notes/', CreateAPIView.as_view(), name="get_note"),
    path('delete_notes/<pk>/', CreateAPIView.as_view(), name="delete_note"),
    path('update_notes/<int:pk>/', UpdateNotesAPIView.as_view(), name="Update_notes"),
    path('create_label/', LabelAPIView.as_view(), name="Create Label"),
    path('get_label/', LabelAPIView.as_view(), name="Get Label"),
    path('archive_notes/<pk>', ArchiveNotesAPIView.as_view(), name="archive notes"),
    path('trash_notes/<pk>', TrashNotesAPIView.as_view(), name="Trash Notes"),
    path('remove_trash_notes/<pk>', RemoveTrashNotesAPIView.as_view(), name="Trash Notes"),
    path('pin_notes/<pk>', PinNotesAPIView.as_view(), name="pin notes"),

]
