from django import forms
from django.contrib.auth.models import User
from .models import UserStockDetails

class UserForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ('username','first_name','last_name','email','password')

class UpdateForm(forms.ModelForm):
    class Meta():
        model = UserStockDetails
        fields = ('purchaseDate','quantity')
# class StockForm(forms.ModelForm):
#     class Meta():
#         model = UserStockDetails
#         fields = ('purchaseDate','last_name','email')
