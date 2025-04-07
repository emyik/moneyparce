from django.urls import path
from . import views

urlpatterns = [
    # Add user profile and delete account routes later
    path('signup/', views.signup, name='signup'),
    path('delete/', views.delete_account, name='delete_account'),
]
