from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('',signupView.as_view(),name='signup'),
    path('login/',loginFunc,name='login'),
    path('logout/',logoutFunc,name='logout'),
    path('home/',HomeView.as_view(),name='home'),
    path('home2/',Home2View.as_view(),name='home2'),
    path('tweetCreate/<str:ISBNcode>',TweetCreate,name='tweetCreate'),
    path('SelectedItem/<str:ISBNcode>',SelectedItem,name='SelectedItem'), 
    path('TweetDelete/<int:tweet_pk>',tweet_del,name='TweetDelete'),
    path('CommentDelete/<int:comment_pk>',comment_del,name='CommentDelete'),
    path('profile_edit/<int:pk>',profile_editView.as_view(),name='profile_edit'),
    path('search_user/',SearchUserView.as_view(),name='search_user'),
    path('user_list_of_follow/<int:user_id>/<str:type_of_follow>',return_user_list_of_follow,name='user_list_of_follow'),
    path('tweet_like/',tweet_like_func, name='tweet_like'),
    path('comment_like/',comment_like_func, name='comment_like'),
    path('userPage/<int:pk>',userPageView.as_view(), name='userPage'),
    path('follow/',follow_func, name='follow'),
    path('CreateComment/<int:tweet_pk>',create_comment, name='CreateComment'),
    path('Chat/<int:user_id>', Chat.as_view(), name='Chat'),
    path('chat_room/<uuid:room_id>', chat_room, name='chat_room'),
    path('room/<int:pk>', room, name='room'),
    path('SearchItem/<str:From>',SearchItem.as_view(),name='SearchItem'),
    path('TweetOfItem/<str:ISBNcode>',TweetOfItemView.as_view(),name='TweetOfItem'),
]
