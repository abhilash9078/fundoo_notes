from django.urls import path
from labels.views import LabelAPIView


urlpatterns = [
    path('create_label/', LabelAPIView.as_view(), name="Create Label"),
    path('get_label/', LabelAPIView.as_view(), name="Get Label"),

]