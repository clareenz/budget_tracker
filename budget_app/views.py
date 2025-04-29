from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, EntryForm
from django.utils import timezone
from django.db.models import Sum
from .models import Entry
from django.shortcuts import render, redirect, get_object_or_404
from calendar import month_name
import csv
from django.http import HttpResponse

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
    # Get filter parameters
    selected_month = request.GET.get('month', '')
    selected_year = request.GET.get('year', '')
    selected_category = request.GET.get('category', '')
    
    # Initialize filter flag
    is_filtered = bool(selected_month or selected_year or selected_category)
    
    # Default to current month if no filters applied
    today = timezone.now().date()
    
    if not is_filtered:
        # Default to current month's data (your original behavior)
        month_start = today.replace(day=1)
        entries = Entry.objects.filter(user=request.user, date__gte=month_start)
    else:
        # Start with all user entries
        entries = Entry.objects.filter(user=request.user)
        
        # Apply filters if provided
        if selected_month:
            entries = entries.filter(date__month=selected_month)
        
        if selected_year:
            entries = entries.filter(date__year=selected_year)
        
        if selected_category:
            entries = entries.filter(category=selected_category)
    
    # Calculate totals
    total_income = entries.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = entries.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense
    
    # Group expenses by category
    category_expenses = {}
    expense_entries = entries.filter(type='expense')
    
    for entry in expense_entries:
        category_name = entry.get_category_display()  # Get human-readable category name
        if category_name in category_expenses:
            category_expenses[category_name] += entry.amount
        else:
            category_expenses[category_name] = entry.amount
    
    # Sort categories by expense amount (descending)
    category_expenses = dict(sorted(category_expenses.items(), key=lambda item: item[1], reverse=True))
    
    # Prepare data for pie chart
    category_names = list(category_expenses.keys())
    category_totals = [float(value) for value in category_expenses.values()]  # Convert to float
    
    # Get available years for the filter dropdown without using ExtractYear
    distinct_years = set()
    for entry in Entry.objects.filter(user=request.user):
        distinct_years.add(entry.date.year)
    available_years = sorted(list(distinct_years), reverse=True)
    available_years = [str(year) for year in available_years]
    
    # Get all categories for the filter dropdown
    all_categories = list(set([entry.get_category_display() for entry in Entry.objects.filter(user=request.user)]))
    all_categories.sort()
    
    # Get month name for display in the active filters
    selected_month_name = month_name[int(selected_month)] if selected_month and selected_month.isdigit() and 1 <= int(selected_month) <= 12 else ""
    
    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'category_expenses': category_expenses,
        'entries': entries.order_by('-date')[:5],  # Most recent entries
        'category_names': category_names,
        'category_totals': category_totals,
        'available_years': available_years,
        'all_categories': all_categories,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'selected_category': selected_category,
        'selected_month_name': selected_month_name,
        'is_filtered': is_filtered,
    }
    
    return render(request, 'budget_app/dashboard.html', context)


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
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="budget_history.csv"'
    
    # Get all entries for the current user
    entries = Entry.objects.filter(user=request.user).order_by('-date')
    
    # Create the CSV writer
    writer = csv.writer(response)
    
    # Write the header row
    writer.writerow(['Title', 'Amount', 'Date', 'Type', 'Category', 'Notes'])
    
    # Write the data rows
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