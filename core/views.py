# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Transaction, Budget, Category
from .forms import TransactionForm

@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    budgets = Budget.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)
    return render(request, 'core/dashboard.html', {
        'transactions': transactions,
        'budgets': budgets,
        'categories': categories,
    })

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'core/add_transaction.html', {'form': form})
