from django import forms

from models import Comment, Reply
from django.contrib.auth import authenticate,get_user_model ,login

User=get_user_model()

class UserLoginForm(forms.Form):

    class Meta:
        model = User
        fields = [

            'username',
            'password'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'id': 'username',
                'required': True,
                'placeholder': 'username',
                'class': "form-control"
            }),

            'password': forms.TextInput(attrs={
                'id': 'password',
                'required': True,
                'placeholder': 'password',
                'class': "form-control"
            }),
        }

    def clean(self, *args,**kwargs):
        username=self.cleaned_data.get("username")
        password=self.cleaned_data.get("password")

        if username and password:
            User = authenticate(username=username, password=password)

            if not User:
                raise forms.ValidationError("this user not exist")
            if not User.check_password(password):
                raise forms.ValidationError("incorrect password")

        return super(UserLoginForm , self).clean(*args,**kwargs)


class UserRegForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    cpassword = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    class Meta:

        model=User
        fields=[
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'cpassword'
        ]

    def clean_cpassword(self):
        password=self.cleaned_data.get('password')
        cpassword = self.cleaned_data.get('cpassword')

        if password!=cpassword :
            raise forms.ValidationError("Password must match")

        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email addresses must be unique.')
        return email


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={
                'id': 'comment-text',
                'required': True,
                'placeholder': 'Leave positive words...',
                'class': "form-control"
            }),
        }

        labels = {

            'comment_text': 'Leave a comment',

        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply

        fields = ['reply_text']
        widgets = {
            'reply_text': forms.TextInput(attrs={
                'id': 'reply-text',
                'required': True,
                'placeholder': 'Make your words positive...',
                'class': "form-control",
            }),
        }






