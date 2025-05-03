from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, EntryForm, BudgetForm
from django.utils import timezone
from django.db.models import Sum
from .models import Budget, Entry
from calendar import month_name
from datetime import datetime
from django.http import HttpResponse
import csv
import json


def home(request):
    return render(request, 'budget_app/home.html')

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
    selected_month = request.GET.get('month', '')
    selected_year = request.GET.get('year', '')
    selected_category = request.GET.get('category', '')
    is_filtered = bool(selected_month or selected_year or selected_category)

    now = timezone.now()

    if not is_filtered:
        entries = Entry.objects.filter(user=request.user, date__month=now.month, date__year=now.year)
    else:
        entries = Entry.objects.filter(user=request.user)
        if selected_month:
            entries = entries.filter(date__month=selected_month)
        if selected_year:
            entries = entries.filter(date__year=selected_year)
        if selected_category:
            entries = entries.filter(category=selected_category)

    total_income = entries.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = entries.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense

    category_expenses = {}
    expense_entries = entries.filter(type='expense')
    for entry in expense_entries:
        label = entry.get_category_display()
        category_expenses[label] = category_expenses.get(label, 0) + entry.amount

    category_expenses = dict(sorted(category_expenses.items(), key=lambda x: x[1], reverse=True))
    category_names = list(category_expenses.keys())
    category_totals = [float(val) for val in category_expenses.values()]

    distinct_years = sorted({e.date.year for e in Entry.objects.filter(user=request.user)}, reverse=True)
    available_years = [str(y) for y in distinct_years]
    all_categories = sorted({e.get_category_display() for e in Entry.objects.filter(user=request.user)})

    over_budget = {}
    budgets = Budget.objects.filter(user=request.user, month=now.month, year=now.year)
    for budget in budgets:
        label = budget.get_category_display()
        spent = sum(e.amount for e in expense_entries if e.category == budget.category)
        if spent > float(budget.amount):
            over_budget[label] = {'total': spent, 'budget': float(budget.amount)}

    context = {
        'entries': entries.order_by('-date')[:5],
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_expenses': category_expenses,
        'category_names': json.dumps(category_names),
        'category_totals': json.dumps(category_totals),
        'available_years': available_years,
        'all_categories': all_categories,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'selected_category': selected_category,
        'selected_month_name': month_name[int(selected_month)] if selected_month.isdigit() else '',
        'is_filtered': is_filtered,
        'over_budget': over_budget,
    }

    return render(request, 'budget_app/dashboard.html', context)

@login_required
def budget_settings(request):
    if request.method == "POST":
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('dashboard')
    else:
        form = BudgetForm()

    return render(request, 'budget_app/budget_settings.html', {'form': form})

@login_required
def history(request):
    entries = Entry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'budget_app/history.html', {'entries': entries})

@login_required
def update_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)

    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, "Entry updated successfully.")
            return redirect('history')
    else:
        form = EntryForm(instance=entry)

    return render(request, 'budget_app/update_entry.html', {'form': form, 'entry': entry})

@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id, user=request.user)

    if request.method == 'POST':
        entry.delete()
        messages.success(request, "Entry deleted successfully.")
        return redirect('history')

    return render(request, 'budget_app/delete_entry.html', {'entry': entry})

@login_required
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="budget_history.csv"'

    entries = Entry.objects.filter(user=request.user).order_by('-date')

    writer = csv.writer(response)
    writer.writerow(['Title', 'Amount', 'Date', 'Type', 'Category', 'Notes'])

    for entry in entries:
        writer.writerow([
            entry.title,
            entry.amount,
            entry.date,
            entry.get_type_display(),
            entry.get_category_display(),
            entry.notes
        ])

    return response

@login_required
def budget_summary(request):
    now = datetime.now()
    budgets = Budget.objects.filter(user=request.user, month=now.month, year=now.year)
    entries = Entry.objects.filter(user=request.user, type='expense', date__month=now.month, date__year=now.year)

    expenses = {}
    for entry in entries:
        expenses[entry.category] = expenses.get(entry.category, 0) + entry.amount

    summary = []
    for budget in budgets:
        spent = expenses.get(budget.category, 0)
        summary.append({
            'category': budget.get_category_display(),
            'budgeted': budget.amount,
            'spent': spent,
            'remaining': budget.amount - spent,
            'over_budget': spent > budget.amount,
        })

    return render(request, 'budget_app/budget_summary.html', {
        'summary': summary,
        'month': now.month,
        'year': now.year,
    })
