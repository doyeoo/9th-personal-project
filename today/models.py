from typing import Match
from django.db import models
from django.db.models.deletion import CASCADE
from django.conf import settings
import datetime
# Create your models here.;


class Hashtag(models.Model):
    hashtag_name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.hashtag_name


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100, blank=True, null=True)
    pub_date = models.DateField('data published', blank=True, null=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True, null=True)
    body = models.TextField(max_length=500, blank=True, null=True)
    image=models.ImageField(upload_to='images/', blank=True, null=True)
    bookmark=models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='bookmark'
    )

    def __str__(self):
        return self.title    

class Schedule(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='schedules', blank=True, null=True)
    start_time = models.TimeField(default=datetime.time(00, 00))
    end_time = models.TimeField(default=datetime.time(00, 00))
    contents = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.post} {self.start_time}-{self.end_time}"
 