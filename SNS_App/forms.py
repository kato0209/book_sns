from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.core.exceptions import ValidationError
from .models import TweetModel,Comment

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