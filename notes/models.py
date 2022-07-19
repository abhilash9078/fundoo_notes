from django.db import models
from user.models import User
from labels.models import Labels


class Notes(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(max_length=1500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    modified_dt = models.DateTimeField(auto_now=True)
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    label = models.ManyToManyField(Labels)
    is_archive = models.BooleanField(default=False)
    is_trash = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_pinned = models.BooleanField(default=False)
    url = models.URLField(blank=True)
    reminder = models.DateTimeField(blank=True, null=True)
    image = models.ImageField()
    color = models.CharField(default=None, max_length=50, blank=True, null=True)

    class Meta:
        ordering = ['-is_pinned', '-id']

    def __str__(self):
        return self.title

    def to_json(self):
        notes = dict()
        notes['title'] = self.title
        notes['description'] = self.description
        notes['label'] = self.label
        return notes

