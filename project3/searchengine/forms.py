from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Email')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UpdateProfileForm(ModelForm):
    class Meta:
        model = Profile
        # exclude = ['user']
        fields = ('image', 'bio')

class UpdateUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

class UpdateFavoriteStreamers(ModelForm):
    class Meta:
        model = Profile
        fields = ['streamer0','streamer1','streamer2','streamer3','streamer4','streamer5','streamer6','streamer7','streamer8','streamer9']


class UpdateFavoriteGames(ModelForm):
    class Meta:
        model = Profile
        fields = ['game0','game1','game2','game3','game4','game5','game6','game7','game8','game9']


