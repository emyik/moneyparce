# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('budgets/add/', views.add_budget, name='add_budget'),
    path('categories/add/', views.add_category, name='add_category'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete_transaction'),
    path('transactions/<int:pk>/edit/', views.edit_transaction, name='edit_transaction'),
    path('budgets/<int:pk>/delete/', views.delete_budget, name='delete_budget'),
    path('budgets/<int:pk>/edit/', views.edit_budget, name='edit_budget'),
    path('categories/<int:pk>/delete/', views.delete_category, name='delete_category'),
    path('categories/manage/', views.category_manager, name='category_manager'),
    path('categories/<int:pk>/edit/', views.edit_category, name='edit_category'),
    path('generate_financial_tips/', views.generate_financial_tips, name='generate_financial_tips'),
]