# forms.py
from django import forms
from .models import *
  
class HotelForm(forms.ModelForm):
  
    class Meta:
        model = item
        fields = ['name', 'category','description','user','initialPrice','closingDate','image','status']