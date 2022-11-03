from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile , Message
from django import forms

#-----------------------------------------------------------------------

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

#-----------------------------------------------------------------------

class ImageForm(ModelForm):
    
    class Meta:
        model = Profile
        fields = ['profile_pic']

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].label = "Choose a new image:"
        self.fields['profile_pic'].placeholder = ""

#-----------------------------------------------------------------------

class MessageForm(ModelForm):
    body = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control border-0","placeholder":"Write a message..."}))
    class Meta:
        model = Message
        fields = ['body']