from django.shortcuts import render, get_object_or_404
from .models import Album, Song
from .forms import UserForm, AlbumForm, SongForm
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q

Image_format = ['png', 'jpeg', 'jpg']
Song_format = ['mp3','wav', 'ogg']

def register(request):
    form = UserForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                all_albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'all_albums': all_albums})

    return render(request, 'music/register.html', {'form': form,})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                all_albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'all_albums': all_albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled.'})

        return render(request, 'music/login.html', {'error_message': 'Username or Password is invalid.'})

    return render(request, 'music/login.html')


def user_logout(request):
    logout(request)
    form = UserForm(request.POST or None, request.FILES or None)

    return render(request, 'music/login.html', {'form': form,})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        all_albums = Album.objects.filter(user=request.user)
        all_songs = Song.objects.all()
        query = request.GET.get('q')
        if query:
            all_albums = all_albums.filter(
                Q(album_name__icontains=query) |
                Q(artist__icontains=query)
            ).distinct()
            all_songs = all_songs.filter(
                Q(song_name__icontains=query)
            ).distinct()
            return render(request, 'music/index.html', {'all_albums': all_albums, 'all_songs': all_songs})

        return render(request, 'music/index.html', {'all_albums': all_albums})

def detail(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/detail.html', {'album': album, 'user': user})


def add_album(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')

    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in Image_format:
                context = {
                    'form': form,
                    'error_message': "Image file must be jpg, jpeg or png."
                }
                return render(request, 'music/album-create.html', context)
            album.save()

            return render(request, 'music/detail.html', {'album': album, })

        return render(request, 'music/album-create.html', {'form': form})


def album_delete(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    all_albums = Album.objects.filter(user=request.user)
    return render(request, 'music/index.html', {'all_albums': all_albums})


def add_song(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = SongForm(request.POST or None, request.FILES or None)
        album = get_object_or_404(Album, pk=album_id)
        if form.is_valid():
            all_songs = album.song_set.all()
            for s in all_songs:
                if s.song_name == form.cleaned_data.get("song_name"):
                    context = {
                        'album': album,
                        'form': form,
                        'error_message': 'Song already exist.'
                    }
                    return render(request, 'music/add-song.html', context)
            song = form.save(commit=False)
            song.album = album
            song.audio_file = request.FILES['audio_file']
            file_type = song.audio_file.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in Song_format:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'File format should be mp3, wav or ogg.'
                }
                return render(request, 'music/add-song.html', context)
            song.save()

            return render(request, 'music/detail.html', {'album': album})

        return render(request, 'music/add-song.html', {'form': form, 'album': album, })


def song_delete(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Song.objects.get(pk=song_id)
    song.delete()
    return render(request, 'music/detail.html', {'album':album})
