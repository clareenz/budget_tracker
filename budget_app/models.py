from django.db import models
from django.contrib.auth.models import User

class Entry(models.Model):
    ENTRY_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]
    
    # Category Choices
    FOOD = 'food'
    HOUSING = 'housing'
    TRANSPORTATION = 'transportation'
    SALARY = 'salary'
    ENTERTAINMENT = 'entertainment'
    OTHERS = 'others'

    CATEGORY_CHOICES = [
        (FOOD, 'Food'),
        (HOUSING, 'Housing'),
        (TRANSPORTATION, 'Transportation'),
        (SALARY, 'Salary'),
        (ENTERTAINMENT, 'Entertainment'),
        (OTHERS, 'Others'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='others')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    type = models.CharField(max_length=7, choices=ENTRY_TYPES)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.amount} ({self.type})"