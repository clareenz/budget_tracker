from django import forms
from .models import Entry
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'amount', 'date', 'type', 'category', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
            'type': forms.Select(attrs={
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 3,
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
        }

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
        }
