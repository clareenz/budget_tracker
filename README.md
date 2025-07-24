# Personal Budget Tracker

This project is a **Personal Budget Tracker** web application that allows users to manage their finances by tracking their income and expenses. Users can register, log in, add income/expense entries, categorize their expenses, and view visual summaries of their financial activities. The application is built with **Django**, **HTML**, **CSS**, **JavaScript**, and **Chart.js**.

### 📝 **CMSC 126 Long Exam 2**

This project is created as part of the **CMSC 126 Long Exam 2**.

# Setup Instructions

## 1. Create virtual Environment
python -m env venv

### On Windows
env\Scripts\activate

### On macOS/Linux
source venv/bin/activate

## 2. Install Dependencies
pip install -r requirements.txt

## 3. Update Database

python manage.py makemigrations

python manage.py migrate

## 4. Run Server
python manage.py runserver