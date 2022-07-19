from rest_framework import serializers
from notes.models import Notes


class NotesSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=4, max_length=400, required=True)
    description = serializers.CharField(min_length=4, max_length=1200, required=True)

    class Meta:
        model = Notes
        fields = '__all__'
        read_only_fields = ['id', 'user', 'is_trash']

    def create(self, validated_data):
        collaborator = validated_data.pop('collaborator')
        label = validated_data.pop('label')
        note = Notes.objects.create(**validated_data)
        note.collaborator.set(collaborator)
        note.label.set(label)
        note.save()
        return note


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




