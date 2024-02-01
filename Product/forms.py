from django import forms
from django.contrib.auth.models import User
from . import models
from Product.models import Product


class ProductForm(forms.ModelForm):
   class Meta:
    model = Product
    fields = ("__all__")


# class BookForm(forms.ModelForm):
#   class Meta:
#     model = Booking
#     fields = ("_all_")


 