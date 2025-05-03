from django import forms
from .models import Entry, Budget
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

MONTH_CHOICES = [
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
]

class BudgetForm(forms.ModelForm):
    month = forms.ChoiceField(choices=MONTH_CHOICES, widget=forms.Select(attrs={
        'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
    }))

    class Meta:
        model = Budget
        fields = ['category', 'amount', 'month', 'year']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
            'year': forms.NumberInput(attrs={
                'placeholder': 'e.g., 2025',
                'class': 'w-full p-3 rounded-xl border border-[#343434] bg-[#3c3c3c] text-[#b1b1b1] text-sm'
            }),
        }
