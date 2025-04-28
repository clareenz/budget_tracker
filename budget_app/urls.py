from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 👈 home page
    path('add/', views.add_entry, name='add_entry'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),  # Note: you had this line duplicated
    path('history/', views.history, name='history'),
    path('entries/<int:entry_id>/update/', views.update_entry, name='update_entry'),
    path('entries/<int:entry_id>/delete/', views.delete_entry, name='delete_entry'),
]