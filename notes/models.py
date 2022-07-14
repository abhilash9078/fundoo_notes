from django.db import models
from user.models import User


class Labels(models.Model):
    label = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.label

    REQUIRED_FIELDS = ['label']


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

    def __str__(self):
        return self.title

