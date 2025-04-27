from django.urls import path
from . import views

urlpatterns = [
    # Add user profile and delete account routes later
    path('signup/', views.signup, name='signup'),
    path('delete/', views.delete_account, name='delete_account'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('password_reset/done/', views.password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete, name='password_reset_complete'),

]
