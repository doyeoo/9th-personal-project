from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser
from django import forms

class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label='비밀번호',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'nickname', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'아이디'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'이름'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'닉네임'}),
        }
        labels = {
            'username': '아이디',
            'name': '이름',
            'nickname': '닉네임',
        }

class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']