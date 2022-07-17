from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.db import IntegrityError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import *
from .forms import *
from django.urls import reverse_lazy,reverse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponseRedirect, HttpResponse
from django.template import loader
import requests
import json
import os
import environ
from SNS_project import settings 
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode

class SignupView(generic.CreateView):
    model=get_user_model()
    form_class=CustomUserCreationForm
    template_name='signup.html'
    success_url = reverse_lazy('login')

def login_func(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
            
        else:
            return render(request,'login.html',{'error':'ユーザ名、パスワードが間違っています。'})

    return render(request,'login.html')


def logout_func(request):
    logout(request)
    return redirect('login')

@login_required
def password_change(request):
    if request.method=='GET':
        form=MyPasswordChangeForm(user=request.user)
        context={
            'form':form,
        }
        return render(request, 'password_change.html', context)
    elif request.method=='POST':
        form=MyPasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('PasswordChangeDone')
        else:
            return render(request, 'password_change.html', {'form':form})

@login_required
def passeword_change_done(request):
    return render(request, 'password_change_done.html')


def password_reset(request):
    template_name='password_reset.html'
    email_template_name='password_reset_message.txt'
    subject_template_name='password_reset_subject.txt'
    password_reset_form=MyPasswordResetForm
    token_generator=default_token_generator

    if request.method=='GET':
        form=password_reset_form()
        context={'form':form}
        return render(request, template_name, context)
    elif request.method=='POST':
        form=password_reset_form(request.POST)
        if form.is_valid():
            context={
                'use_https':request.is_secure(),
                'token_generator':token_generator,
                'from_email':settings.FROM_EMAIL,
                'email_template_name':email_template_name,
                'subject_template_name':subject_template_name,
                'request':request,
            }
            context['domain_override']=request.get_host()
            form.save(**context)
            return redirect('PasswordResetDone')
        else:
            print(100)
            context={'form':form}
            return render(request, 'password_reset.html', context)

def password_reset_done(request):
    return render(request, 'password_reset_done.html')

def password_reset_confirm(request, uidb64, token):
    template_name='password_reset_confirm.html'
    token_generator=default_token_generator
    set_password_form=MySetPasswordForm

    user_model=get_user_model()
    assert uidb64 is not None and token is not None
    try:
        user_id=force_text(urlsafe_base64_decode(uidb64))
        user=user_model.objects.get(pk=user_id)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user=None
    if user is not None and token_generator.check_token(user, token):
        if request.method == 'POST':
            form=set_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect('PasswordResetComplete')
        else:
            form=set_password_form(user)
    else:
        form=None
    
    return render(request, template_name, {'form':form})

def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')


class HomeView(LoginRequiredMixin,generic.ListView):
    model=TweetModel
    template_name='home.html'
    context_object_name = 'tweetmodel_list'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset=queryset.exclude(user=self.request.user)
        keyword=self.request.GET.get('keyword')
        if keyword:
            queryset=queryset.filter(content__icontains=keyword)
        
        return queryset[:1000]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        selected_page='home'
        liked_list = []

        for tweet in context['tweetmodel_list']:
            liked = tweet.like_set.filter(user=self.request.user)
            if liked.exists():
                liked_list.append(tweet.id)
        
        context['liked_list']=liked_list
        context['selected_page']=selected_page
        return context

class Home2View(LoginRequiredMixin,generic.ListView):
    model=TweetModel
    template_name='home.html'
    context_object_name = 'tweetmodel_list'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset=queryset.exclude(user=self.request.user)
        Connections=self.request.user.following.all()
        following_list=[]
        for connection in Connections:
            following_list.append(connection.followed)
        queryset=queryset.filter(user__in=following_list).order_by('created_at')
        keyword=self.request.GET.get('keyword')
        if keyword:
            queryset=queryset.filter(content__icontains=keyword)
        
        return queryset[:1000]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        selected_page='home2'
        liked_list = []

        for tweet in context['tweetmodel_list']:
            liked = tweet.like_set.filter(user=self.request.user)
            if liked.exists():
                liked_list.append(tweet.id)
        
        context['liked_list']=liked_list
        context['selected_page']=selected_page
        return context

@login_required
def tweet_create(request,ISBNcode):
    if request.method == "POST":
        form=TweetCreationForm(request.POST)
        book=BookData.objects.get(ISBNcode=ISBNcode)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user = request.user   
            tweet.book=book
            tweet.save()
            return redirect('home')
        else:
            book_title=book.title
            return render(request,'tweet_create.html',{'form':form,'ISBNcode':ISBNcode,'book_title':book_title})
    else:
        form=TweetCreationForm()
        book=BookData.objects.get(ISBNcode=ISBNcode)
        book_title=book.title
        return render(request,'tweet_create.html',{'form':form,'ISBNcode':ISBNcode,'book_title':book_title})

@login_required
def select_item(request,ISBNcode):
    Item=get_api_data(params={'isbn':ISBNcode})
    item=Item[0]['Item']
    book=BookData.objects.filter(ISBNcode=ISBNcode)
    if book.exists():
        book=book[0]
        book.title=item['title']
        book.author=item['author']
        book.itemPrice=item['itemPrice']
        book.itemUrl=item['itemUrl']
        book.ImageUrl=item['largeImageUrl']
    else:
        book.create(
            ISBNcode=ISBNcode,
            title=item['title'],
            author=item['author'],
            itemPrice=item['itemPrice'],
            itemUrl=item['itemUrl'],
            imageUrl=item['largeImageUrl']
        )
    return redirect(reverse('tweetCreate', args=[ISBNcode]))
        

@login_required
def tweet_del(request, tweet_pk):
    tweet = get_object_or_404(TweetModel, pk=tweet_pk)
    tweet.delete()
    return redirect(request.META['HTTP_REFERER'])

@login_required
def comment_del(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    comment.delete()
    return redirect(request.META['HTTP_REFERER'])

class profile_editView(LoginRequiredMixin,generic.UpdateView):
    model=get_user_model()
    form_class=CustomUserChangeForm
    template_name='profile_edit.html'
    success_url = reverse_lazy('home')


class SearchUserView(LoginRequiredMixin,generic.ListView):
    model=CustomUser
    template_name='search_user.html'
    context_object_name = 'user_list'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset(**kwargs)
        keyword_user=self.request.GET.get('keyword_user')
        if keyword_user:
            queryset=queryset.filter(username__icontains=keyword_user)
            return queryset
        else:
            return CustomUser.objects.none()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        following_list=[]

        for searched_user in context['user_list']:
            followed_connections=searched_user.followed.all()
            followed = followed_connections.filter(following=self.request.user)
            if followed.exists():
                following_list.append(searched_user.id)

        context['following_list']=following_list
        
        return context

def follower_show(request, user_id):
    selected_user=CustomUser.objects.get(id=user_id)
    user_list=[]
    user_list_connection=selected_user.followed.all()
    for connection in user_list_connection:
        user_list.append(connection.following)
    following_list=[]
    for user in user_list:
        followed_connections=user.followed.all()
        followed = followed_connections.filter(following=request.user)
        if followed.exists():
            following_list.append(user.id)
    
    context={
        'user_list':user_list,
        'following_list':following_list,
        'type':'follower',
    }
    return render(request,'user_list_of_follow.html',context)

def following_show(request, user_id):
    selected_user=CustomUser.objects.get(id=user_id)
    user_list=[]
    user_list_connection=selected_user.following.all()
    for connection in user_list_connection:
        user_list.append(connection.followed)
    following_list=[]
    for user in user_list:
        followed_connections=user.followed.all()
        followed = followed_connections.filter(following=request.user)
        if followed.exists():
            following_list.append(user.id)
    
    context={
        'user_list':user_list,
        'following_list':following_list,
        'type':'following',
    }
    return render(request,'user_list_of_follow.html',context)
            

@login_required
def tweet_like_func(request):
    if request.method =="POST":
        like_id=json.loads(request.body).get('like_id')
        tweet = get_object_or_404(TweetModel, pk=like_id)
        user=request.user
        liked = False
        like = Like.objects.filter(tweet=tweet, user=user)
        if like.exists():
            like.delete()
        else:
            like.create(tweet=tweet, user=user)
            liked = True

        count=tweet.like_set.count()
        context={
            'like_id': like_id,
            'liked': liked,
            'count': count,
            }
    if request.is_ajax():
        return JsonResponse(context)

@login_required
def comment_like_func(request):
    if request.method =="POST":
        like_id=json.loads(request.body).get('like_id')
        comment = get_object_or_404(Comment, pk=like_id)
        user=request.user
        liked = False
        like = Like.objects.filter(user=user,comment=comment)
        if like.exists():
            like.delete()
        else:
            like.create(user=user,comment=comment)
            liked = True

        count=comment.like_set.count()
        context={
            'like_id': like_id,
            'liked': liked,
            'count': count,
            }
    if request.is_ajax():
        return JsonResponse(context)


class userPageView(LoginRequiredMixin,generic.ListView):
    model=TweetModel
    template_name='user_page.html'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset(**kwargs)
        selected_user = CustomUser.objects.get(id=self.kwargs['pk'])
        queryset=queryset.filter(user=selected_user)
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        liked_list = []
        followed=False
        selected_user = CustomUser.objects.get(id=self.kwargs['pk'])
        selected_user_following_count=selected_user.following.count()
        selected_user_followed_count=selected_user.followed.count()
        following_list=self.request.user.following.all() 
        
        followed=following_list.filter(followed=selected_user)
        if followed.exists():
            followed=True

        for tweet in context['object_list']:
            liked = tweet.like_set.filter(user=self.request.user)
            if liked.exists():
                liked_list.append(tweet.id)

        context['selected_user_following_count']=selected_user_following_count
        context['selected_user_followed_count']=selected_user_followed_count
        context['selected_user']=selected_user
        context['liked_list']=liked_list
        context['followed']=followed
        
        return context


@login_required
def follow_func(request):
    if request.method =="POST":
        following = request.user
        follow_id=json.loads(request.body).get('follow_id')
        from_user_page=False
        from_user_page=json.loads(request.body).get('from_user_page')
        followed_user = CustomUser.objects.get(pk=follow_id)
        followed=False
        connection = Connection.objects.filter(followed=followed_user,following=following)

        if connection.exists():
            connection.delete()
        else:
            connection.create(followed=followed_user, following=following)
            followed = True

        if from_user_page:
            follower_count=followed_user.followed.count()
            context={
            'follow_id': follow_id,
            'followed': followed,
            'follower_count': follower_count,
            }
        else:
            context={
                'follow_id': follow_id,
                'followed': followed,
            }
        
    if request.is_ajax():
        return JsonResponse(context)

@login_required
def create_comment(request, tweet_pk):
    if request.method=="GET":
        form=CreateCommentForm()
        tweet=TweetModel.objects.filter(id=tweet_pk)
        if not tweet.exists():
            return redirect('home')
        tweet=tweet[0]
        comment_list=tweet.comment_set.all()
        liked_list = []
        for comment in comment_list:
            liked = comment.like_set.filter(user=request.user)
            if liked.exists():
                liked_list.append(comment.id)
        liked=False
        if tweet.like_set.filter(user=request.user):
            liked=True
        context={
            'tweet':tweet,
            'comment_list':comment_list,
            'liked_list':liked_list,
            'liked':liked,
            'form':form
        }
        return render(request,'Comment.html',context)
    else:
        form=CreateCommentForm(request.POST)
        comment=form.save(commit=False)
        comment.user = request.user
        comment.tweet=TweetModel.objects.get(id=tweet_pk)
        comment.save()
        return redirect(request.META['HTTP_REFERER'])

class Chat(LoginRequiredMixin,generic.ListView):
    model=Room
    template_name='chat.html'
    context_object_name = 'room_list'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset(**kwargs).order_by('-created_at')
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        partner_list=[]
        message_list=[]
        room_list=[]
        partner_dict={}
        user=CustomUser.objects.get(id=self.kwargs['user_id'])
        entries=Entries.objects.filter(user=user).order_by('-joined_at')
        for entry in entries:
            room_list.append(entry.room)

        for room in room_list:
            partner=room.room_member.all().exclude(id=user.id)[0]
            if room.message_set:
                message=room.message_set.order_by('-created_at')[0]
                message_list.append(message)
                partner_list.append(partner)
            
        partner_dict=dict(zip(partner_list,message_list))
        context['partner_dict']=partner_dict
        return context 

@login_required
def chat_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.user in room.room_member.all():
        Partner=room.room_member.all().exclude(id=request.user.id)[0]
        messages = Message.objects.filter(room=room).order_by('created_at')
        context = {
            'messages':messages,
            'room': room,
            'Partner':Partner,
            'WS_URL':settings.WS_URL,
        }
        return render(request,'chat_room.html',context)

    return redirect(reverse('Chat', args=[request.user.id]))

    

@login_required
def room(request,pk):
    User1=request.user
    User2=CustomUser.objects.get(pk=pk)
    roomQuery=Room.objects.filter(room_member=User1).filter(room_member=User2)
    if not roomQuery.exists():
        room = Room.objects.create()
        room.room_member.add(User1)
        room.room_member.add(User2)
    else:
        room=roomQuery[0]

    return redirect(reverse('chat_room', args=[room.id]))

#RakutenAPI
SEARCH_URL='https://app.rakuten.co.jp/services/api/BooksBook/Search/20170404?format=json&applicationId='+settings.APPLICARIONID

def get_api_data(params):
        api=requests.get(SEARCH_URL,params=params).text
        result=json.loads(api)
        items=result['Items']
        return items

class SearchItem(LoginRequiredMixin,generic.View):
    def get(self, request, *args, **kwargs):
        From=self.kwargs['From']
        form=RakutenSearchForm()
        category_list=[]
        for category in form['category']:
            category_list.append(category)
        return render(request,'item_search.html',{'form':form,'From':From,'category_list':category_list})

    def post(self, request, *args, **kwargs):
        form=RakutenSearchForm(request.POST or None)
        From=self.kwargs['From']
        if form.is_valid():
            keyword=form.cleaned_data['title']
            booksGenreId=form.cleaned_data['category']
            page_number=form.cleaned_data['page_number']
            if booksGenreId and keyword:
                params={
                'title':keyword,
                'booksGenreId':booksGenreId,
                'outOfStockFlag':1,
                'page':page_number,
            }
            elif keyword:
                params={
                'title':keyword,
                'outOfStockFlag':1,
                'page':page_number,
            }
            elif booksGenreId:
                params={
                'booksGenreId':booksGenreId,
                'outOfStockFlag':1,
                'page':page_number,
            }
            else:
                params={
                'outOfStockFlag':1,
                'page':page_number,
            }
            items=get_api_data(params)
            book_data=[]
            for i in items:
                item=i['Item']
                title=item['title']
                image=item['largeImageUrl']
                author=item['author']
                itemPrice=item['itemPrice']
                ISBNcode=item['isbn']
                itemUrl=item['itemUrl']
                query={
                    'title':title,
                    'image':image,
                    'author':author,
                    'itemPrice':itemPrice,
                    'ISBNcode':ISBNcode,
                    'itemUrl':itemUrl,
                }
                book_data.append(query)
            for_range = [i for i in range(1,11)]
            return render(request,'item_list.html',{
                'book_data':book_data,
                'keyword':keyword,
                'form':form,
                'booksGenreId':booksGenreId,
                'From':From,
                'page_number':page_number,
                'for_range':for_range,
            })
        return render(request,'item_search.html',{
            'form':form,
            'From':From,
        })

class TweetOfItemView(LoginRequiredMixin,generic.ListView):
    model=TweetModel
    template_name='tweet_of_item.html'
    context_object_name = 'tweetmodel_list'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset(**kwargs)
        queryset=queryset.filter(book__ISBNcode=self.kwargs['ISBNcode']).order_by('-created_at')
        return queryset
