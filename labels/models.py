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

