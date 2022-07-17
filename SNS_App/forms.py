from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
from .models import TweetModel,Comment
import re
from django.contrib.auth.forms import PasswordChangeForm,PasswordResetForm,SetPasswordForm
from django.template import loader

def isalnum(password):
    password_reg=re.compile('\A(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)[a-zA-Z\d]{8,100}\Z')
    return password_reg.match(password) is not None

class CustomUserCreationForm(forms.ModelForm):

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder': 'パスワード'}))
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(attrs={'class' : 'form-control','placeholder': 'パスワード(再入力)'}))


    def clean_password1(self):
        password1 = self.cleaned_data.get("password1")
        if isalnum(password1):
            return password1
        else:
            raise forms.ValidationError('※半角英小文字大文字数字をそれぞれ1種類以上含む8文字以上100文字以下の\nパスワードを設定して下さい')


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('※1回目とパスワードが異なります')
        else:
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

class MyPasswordChangeForm(PasswordChangeForm):

    error_messages={
        'password_incorrect':'※元のパスワードが間違っています。もう一度入力してください。'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class' : 'form-control','autofocus' : 'autofocus'})
        self.fields['new_password1'].widget.attrs.update({'class' : 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class':'form-control'})

    def clean_new_password1(self):
        new_password1=self.cleaned_data.get('new_password1')
        if isalnum(new_password1):
            return new_password1
        else:
            raise forms.ValidationError('※半角英小文字大文字数字をそれぞれ1種類以上含む8文字以上100文字以下の\nパスワードを設定して下さい')

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('※1回目とパスワードが異なります')
        else:
            return new_password2

class MyPasswordResetForm(PasswordResetForm):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class' : 'form-control','placeholder': 'メールアドレス'}))

    def clean_email(self):
        email=self.cleaned_data.get('email')
        users=self.get_users(email)
        user=None
        for user_ in users:
            user=user_
        if not user:
            raise forms.ValidationError('有効なメールアドレスを入力してください。')
        else:
            return email

class MySetPasswordForm(SetPasswordForm):
   
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({'class' : 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class':'form-control'})

    def clean_new_password1(self):
        new_password1=self.cleaned_data.get('new_password1')
        if isalnum(new_password1):
            return new_password1
        else:
            raise forms.ValidationError('※半角英小文字大文字数字をそれぞれ1種類以上含む8文字以上100文字以下の\nパスワードを設定して下さい')

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")
        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('※1回目とパスワードが異なります')
        else:
            return new_password2

class TweetCreationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TweetCreationForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({'class' : 'form-control','placeholder':'感想を書こう!','autofocus' : 'autofocus'})
        self.fields['rating'].widget.attrs.update({'class':'d-transparent'})
        
    
    class Meta:
        model = TweetModel
        fields = '__all__'

        labels = {
                  'content':"本文",
                  'snsImage':"画像",
        }

        error_messages = {
            "content": {
                "required": "本文が入力されていません",
            },
            "rating": {
                "required": "評価を選んで下さい",
            },
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
        self.fields['text'].widget.attrs.update({'class' : 'form-control','placeholder':'コメントを書く','id':'comment_input'})

    class Meta:
        model = Comment
        fields = ('text',)
    
class RakutenSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(RakutenSearchForm, self).__init__(*args, **kwargs)
        self.fields['page_number'].initial = 1
        self.fields['category'].widget.attrs.update({'class' : 'form-select'})

    BOOK_CHOICES = (
        ('001', '本全般'),
        ('001004001', 'ミステリー・サスペンス'),
        ('001004002', 'SF・ホラー'),
        ('001004003', 'エッセイ'),
        ('001004004', 'ノンフィクション'),
        ('001004008', '日本の小説'),
        ('001004009', '外国の小説'),
        ('001004016', 'ロマンス'),
        ('001017', 'ライトノベル'),
    )

    category = forms.fields.ChoiceField(
        choices=BOOK_CHOICES,
        required=False,
        label='ジャンル',
    )
    title=forms.CharField(label='タイトル',max_length=200,required=False)
    page_number=forms.IntegerField(widget=forms.HiddenInput)