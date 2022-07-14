from rest_framework import serializers

from notes.models import Notes, Labels


class NotesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=4, max_length=400, required=True)
    description = serializers.CharField(min_length=4, max_length=1200, required=True)

    class Meta:
        model = Notes
        fields = '__all__'
        read_only_fields = ['id', 'user', 'isTrash']


class LabelSerializer(serializers.ModelSerializer):

    label = serializers.CharField(min_length=2, max_length=100, required=True)

    class Meta:
        model = Labels
        fields = ['label']
        read_only_fields = ['id', 'label_id']
        REQUIRED_FIELDS = ['label']

