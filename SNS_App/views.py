from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,get_user_model,login,logout
from django.db import IntegrityError
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

class signupView(generic.CreateView):
    model=get_user_model()
    form_class=CustomUserCreationForm
    template_name='signup.html'
    success_url = reverse_lazy('login')

def loginFunc(request):
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


def logoutFunc(request):
    logout(request)
    return redirect('login')


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
        
        return queryset

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        liked_list = []

        for tweet in context['tweetmodel_list']:
            liked = tweet.like_set.filter(user=self.request.user)
            if liked.exists():
                liked_list.append(tweet.id)
        
        context['liked_list']=liked_list
        return context


@login_required
def TweetCreate(request,ISBNcode):
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
            title=book.title
            return render(request,'tweet_create.html',{'form':form,'ISBNcode':ISBNcode,'title':title})
    else:
        form=TweetCreationForm()
        book=BookData.objects.get(ISBNcode=ISBNcode)
        title=book.title
        return render(request,'tweet_create.html',{'form':form,'ISBNcode':ISBNcode,'title':title})

@login_required
def SelectItem(request):
    return render(request,'book_select.html')

@login_required
def SelectedItem(request,ISBNcode):
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
        followed_list=[]

        for searched_user in context['user_list']:
            follower_list=searched_user.follower.all()
            followed = follower_list.filter(following=self.request.user)
            if followed.exists():
                followed_list.append(searched_user.id)

        context['followed_list']=followed_list
        
        return context


@login_required
def LikeFunc(request):
    if request.method =="POST":
        tweet=None
        comment=None
        
        like_type=request.POST.get('like_type')
        likeInfo=request.POST.get('likeInfo')
        index=likeInfo.find('-')
        id=likeInfo[index+1:]
        if like_type =='tweet':
            tweet = get_object_or_404(TweetModel, pk=id)
        elif like_type =='comment':
            comment = get_object_or_404(Comment, pk=id)
        user=request.user
        liked = False
        like = Like.objects.filter(tweet=tweet, user=user,comment=comment)
        if like.exists():
            like.delete()
        else:
            like.create(tweet=tweet, user=user,comment=comment)
            liked = True

        if tweet:
            count=tweet.like_set.count()
        elif comment:
            count=comment.like_set.count()

        context={
            'id': id,
            'liked': liked,
            'like_type':like_type,
            'count': count,
            }
    if request.is_ajax():
        return JsonResponse(context)


class userPageView(LoginRequiredMixin,generic.ListView):
    model=TweetModel
    template_name='userPage.html'

    def get_queryset(self,**kwargs):
        queryset = super().get_queryset(**kwargs)
        tweetUser = CustomUser.objects.get(id=self.kwargs['pk'])
        queryset=queryset.filter(user=tweetUser)
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        liked_list = []
        followed=False
        tweetUser = CustomUser.objects.get(id=self.kwargs['pk'])
        following_list=self.request.user.following.all() 
        
        followed=following_list.filter(follower=tweetUser)
        if followed.exists():
            followed=True

        for tweet in context['object_list']:
            liked = tweet.like_set.filter(user=self.request.user)
            if liked.exists():
                liked_list.append(tweet.id)

        context['tweetUser']=tweetUser
        context['liked_list']=liked_list
        context['followed']=followed
        
        return context


@login_required
def FollowFunc(request):
    if request.method =="POST":
        following = request.user
        follower = CustomUser.objects.get(pk=request.POST.get('user_id'))
        
        followed=False
        connection = Connection.objects.filter(follower=follower,following=following)

        if connection.exists():
            connection.delete()
        else:
            connection.create(follower=follower, following=following)
            followed = True
    
        context={
            'user_id': follower.id,
            'followed': followed,
        }
        
    if request.is_ajax():
        return JsonResponse(context)

class CreateComment(LoginRequiredMixin,generic.CreateView):
    model=Comment
    form_class=CreateCommentForm
    template_name='Comment.html'

    def get_success_url(self):
        url=self.request.META['HTTP_REFERER']
        return url
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tweet']=TweetModel.objects.get(id=self.kwargs['tweet_pk'])
        comment_list=context['tweet'].comment_set.all()
        context['comment_list']=comment_list
        liked_list = []

        for comment in context['comment_list']:
            liked = comment.like_set.filter(user=self.request.user)
            if liked.exists():
                liked_list.append(comment.id)

        context['liked_list']=liked_list

        liked=False
        if context['tweet'].like_set.filter(user=self.request.user):
            liked=True
        context['liked']=liked
        
        return context

    def form_valid(self, form):
        comment=form.save(commit=False)
        comment.user = self.request.user
        comment.tweet=TweetModel.objects.get(id=self.kwargs['tweet_pk'])
        comment.save()
        return super().form_valid(form)

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
            message=room.message_set.order_by('-created_at')[0]
            partner_list.append(partner)
            message_list.append(message)
        
        partner_dict=dict(zip(partner_list,message_list))
        context['room_list']=room_list
        context['partner_dict']=partner_dict
        return context


def chat_room(request, room_id,user_id):
    room = Room.objects.get(id=room_id)
    Partner=CustomUser.objects.get(pk=user_id)
    messages = Message.objects.filter(room=room).order_by('created_at')
    template = loader.get_template('chat_room.html')
    context = {
        'messages':messages,
        'room': room,
        'Partner':Partner
    }
    return HttpResponse(template.render(context, request))

@login_required
def room(request,pk):
    User1=request.user
    User2=CustomUser.objects.get(pk=pk)
    member_list=[User1,User2]
    roomQuery=Room.objects.filter(room_member=User1).filter(room_member=User2)
    if not roomQuery.exists():
        room = Room.objects.create()
        room.room_member.add(User1)
        room.room_member.add(User2)
    else:
        room=roomQuery[0]

    return HttpResponseRedirect(reverse('chat_room', args=[room.id,User2.id]))

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
        return render(request,'Item-search.html',{'form':form,'From':From})

    def post(self, request, *args, **kwargs):
        form=RakutenSearchForm(request.POST or None)
        From=self.kwargs['From']
        if form.is_valid():
            keyword=form.cleaned_data['title']
            booksGenreId=form.cleaned_data['category']
            page=form.cleaned_data['page']
            if booksGenreId and keyword:
                params={
                'title':keyword,
                'booksGenreId':booksGenreId,
                'outOfStockFlag':1,
                'page':page,
            }
            elif keyword:
                params={
                'title':keyword,
                'outOfStockFlag':1,
                'page':page,
            }
            elif booksGenreId:
                params={
                'booksGenreId':booksGenreId,
                'outOfStockFlag':1,
                'page':page,
            }
            else:
                params={
                'outOfStockFlag':1,
                'page':page,
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
            return render(request,'Itemlist.html',{
                'book_data':book_data,
                'keyword':keyword,
                'form':form,
                'booksGenreId':booksGenreId,
                'From':From,
                'page':page,
                'for_range':for_range,
            })
        return render(request,'Item-search.html',{
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
