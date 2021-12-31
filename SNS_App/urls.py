from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('signup/',signupView.as_view(),name='signup'),
    path('login/',loginFunc,name='login'),
    path('logout/',logoutFunc,name='logout'),
    path('home/',HomeView.as_view(),name='home'),
    path('tweet/',TweetView.as_view(),name='tweet'),
    path('TweetDelete/<int:tweet_pk>',tweet_del,name='TweetDelete'),
    path('CommentDelete/<int:comment_pk>',comment_del,name='CommentDelete'),
    path('profile_edit/<int:pk>',profile_editView.as_view(),name='profile_edit'),
    path('search_user/',SearchUserView.as_view(),name='search_user'),
    path('like/',LikeFunc, name='like'),
    path('userPage/<int:pk>',userPageView.as_view(), name='userPage'),
    path('follow/',FollowFunc, name='follow'),
    path('CreateComment/<int:tweet_pk>',CreateComment.as_view(), name='CreateComment'),
    path('Chat/<int:user_id>', Chat.as_view(), name='Chat'),
    path('chat_room/<uuid:room_id>/<int:user_id>', chat_room, name='chat_room'),
    path('room/<int:pk>', room, name='room'),
]
