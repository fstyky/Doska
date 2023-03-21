from django.urls import path
from django.shortcuts import redirect

from .views import Content, CreatePost, PostItem, EditPost, DeletePost, Replays, Rep, replay_accept,replay_delete


urlpatterns = [
  path('content', Content.as_view(), name='content'),
  path('post/<int:pk>', PostItem.as_view()),
  path('create_ad', CreatePost.as_view(), name='create_ad'),
  path('post/<int:pk>/edit', EditPost.as_view()),
  path('post/<int:pk>/delete', DeletePost.as_view()),
  path('replay', Replays.as_view(), name='replays'),
  path('replay/<int:pk>', Replays.as_view(), name='replays'),
  path('rep/<int:pk>', Rep.as_view(), name='rep'),
  path('replay/accept/<int:pk>', replay_accept),
  path('replay/delete/<int:pk>', replay_delete),
  path('', lambda request: redirect('index', permanent=False)),
]