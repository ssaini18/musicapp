from django import forms
from .models import Album, Song
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'album_name', 'genre', 'album_logo']

class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ['song_name', 'audio_file']