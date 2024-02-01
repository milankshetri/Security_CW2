from django import forms
from Fulbari.models import Blogs
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
User=get_user_model()






class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class BlogForm(forms.ModelForm): 
    class Meta:
        model = Blogs
        fields = ["blog_name","blog_details","blog_image"]