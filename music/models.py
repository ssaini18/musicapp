from django.db import models
from django.contrib.auth.models import User, Permission

class Album(models.Model):
    user = models.ForeignKey(User, default=1)
    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    album_logo = models.FileField()

    def __str__(self):
        return self.album_name

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    song_name = models.CharField(max_length=100)
    audio_file = models.FileField()

    def __str__(self):
        return self.song_name

