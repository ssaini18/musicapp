from django.conf.urls import url
from . import views


urlpatterns = [
    #
    url(r'^$', views.index, name='index'),
    #register/
    url(r'^register/$', views.register, name='register'),
    #login/
    url(r'^login/$', views.user_login, name='user_login'),
    #logout/
    url(r'^logout/$', views.user_logout, name='user_logout'),
    #music/album/album_id/
    url(r'^album/(?P<album_id>[0-9]+)/$', views.detail, name='detail'),
    #music/create-album/
    url(r'^add-album/$', views.add_album, name='add_album'),
    #music/album-delete/album_id/
    url(r'^album-delete/(?P<album_id>[0-9]+)/$', views.album_delete, name='album_delete'),
    #music/album_id/add-song/
    url(r'^(?P<album_id>[0-9]+)/add-song/$', views.add_song, name='add_song'),
    #music/album_id/song-delete/song_id
    url(r'^(?P<album_id>[0-9]+)/song-delete/(?P<song_id>[0-9]+)/$', views.song_delete, name='song_delete'),

]
