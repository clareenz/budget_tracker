from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, EntryForm
from django.utils import timezone
from django.db.models import Sum
from .models import Entry

def index(request):
    return render(request, 'index.html')

@login_required
def add_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('dashboard')
    else:
        form = EntryForm()
    return render(request, 'budget_app/add_entry.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully.")
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'budget_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'budget_app/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    return render(request, 'budget_app/dashboard.html')


@login_required
def dashboard(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    entries = Entry.objects.filter(user=request.user, date__gte=month_start)

    total_income = entries.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = entries.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    categories = entries.filter(type='expense').values('category__name').annotate(total=Sum('amount'))

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'categories': categories,
        'entries': entries,
    }
    return render(request, 'budget_app/dashboard.html', context)


@login_required
def history(request):
    entries = Entry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'budget_app/history.html', {'entries': entries})