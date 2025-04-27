from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after signup
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('login')
    return render(request, 'registration/delete_account.html')

def password_reset_request(request):
    return auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        success_url='/accounts/password_reset/done/'
    )(request)

def password_reset_done(request):
    return auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password.html'
    )(request)

def password_reset_confirm(request, uidb64, token):
    return auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url='/accounts/reset/done/'
    )(request, uidb64=uidb64, token=token)

def password_reset_complete(request):
    return auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    )(request)
