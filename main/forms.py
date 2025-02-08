from django import forms
from .models import ContactRequest



class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['name', 'phone']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ваше имя',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Номер телефона',
                'type': 'tel',
                'required': True
            }),
        }
        labels = {
            'name': 'Имя',
            'phone': 'Телефон'
        } 