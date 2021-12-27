from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
from .models import TweetModel,Category,Comment


class CustomUserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder': 'パスワード'}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder': 'パスワード(再入力)'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('※1回目とパスワードが異なります')
            
        return password2

    def save(self, commit=True):
        user = super(forms.ModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user   

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class' : 'form-control','placeholder': 'メールアドレス'})
        self.fields['username'].widget.attrs.update({'class' : 'form-control','placeholder': 'ユーザー名'})


    class Meta:
        model = get_user_model()
        fields = ('email','username')


class TweetCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TweetCreationForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class' : 'form-control','placeholder':'タイトル','autofocus' : 'autofocus'})
        self.fields['content'].widget.attrs.update({'class' : 'form-control','placeholder':'ここに文章を入力'})
        self.fields['category'].widget.attrs.update({'class' : 'form-select'})
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='カテゴリを選択してください'
    )

    Choice=(
        (None,'評価'),(1,1),(2,2),(3,3),(4,4),(5,5),
    )
    rating=forms.ChoiceField(choices=Choice,required=True)

    class Meta:
        model = TweetModel
        fields = '__all__'

        labels = {
                  'content':"本文",
                  'snsImage':"画像",
        }


        

class CustomUserChangeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
            super(CustomUserChangeForm, self).__init__(*args, **kwargs)
            self.fields['username'].widget.attrs.update({'class' : 'form-control'})

    ProfileImage= forms.ImageField(widget=forms.widgets.FileInput)

    class Meta:
        model = get_user_model()
        fields = ('username','ProfileImage')

class CreateCommentForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        super(CreateCommentForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({'class' : 'form-control','placeholder':'コメントを書く','id':'CommentForm'})

    class Meta:
        model = Comment
        fields = ('text',)