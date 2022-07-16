# Generated by Django 4.0.6 on 2022-07-15 05:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('labels', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('description', models.TextField(max_length=1500)),
                ('created_dt', models.DateTimeField(auto_now_add=True)),
                ('modified_dt', models.DateTimeField(auto_now=True)),
                ('is_archive', models.BooleanField(default=False)),
                ('is_trash', models.BooleanField(default=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('is_pinned', models.BooleanField(default=False)),
                ('url', models.URLField(blank=True)),
                ('reminder', models.DateTimeField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='')),
                ('color', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('collaborator', models.ManyToManyField(related_name='collaborator', to=settings.AUTH_USER_MODEL)),
                ('label', models.ManyToManyField(to='labels.labels')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
