from rest_framework import serializers

from notes.models import Notes


class NotesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=4, max_length=400, required=True)
    description = serializers.CharField(min_length=4, max_length=1200, required=True)

    class Meta:
        model = Notes
        fields = '__all__'
        read_only_fields = ['id', 'user', 'is_trash']


class TrashSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'is_trash']
        read_only_fields = ['id', 'title']


class PinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = ['id', 'title', 'description', 'is_pinned']
        read_only_fields = ['id', 'title']




