# from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . models import CustomUser
from data.models import Data
from django.forms import ModelForm

# this was created to link with database but latter comment
# class DocumentForm(ModelForm):
#     class Meta:
#         model = Data
#         fields = ['path']
#         exclude = ['id','name','user','created_at']
class CustomUserCreationForm(UserCreationForm):

    class meta:
        model = CustomUser
        fields = ('username','email','name','created_at', 'access_code')

class CustomUserChangeForm(UserChangeForm):
    class meta:
        model = CustomUser
        fields = ('username','email', 'name','created_at', 'access_code')


