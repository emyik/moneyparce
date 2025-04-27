# core/views.py
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import Transaction, Budget, Category
from .forms import TransactionForm
from .forms import BudgetForm
from .forms import CategoryForm
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from dotenv import load_dotenv
import os
from google import genai
from django.db.models import Sum

load_dotenv()

api_key1 = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=api_key1)
@login_required
def dashboard(request):
    categories = Category.objects.filter(user=request.user)
    selected_category_id = request.GET.get('category')
    
    transactions = Transaction.objects.filter(user=request.user)
    if selected_category_id:
        transactions = transactions.filter(category_id=selected_category_id)

    budgets = Budget.objects.filter(user=request.user)

    return render(request, 'core/dashboard.html', {
        'transactions': transactions,
        'budgets': budgets,
        'categories': categories,
        'selected_category_id': selected_category_id
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

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('dashboard')
    else:
        form = BudgetForm()
    return render(request, 'core/add_budget.html', {'form': form})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_manager')
    else:
        form = CategoryForm()
    return render(request, 'core/add_category.html', {'form': form})

@login_required
def transaction_detail(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    return render(request, 'core/transaction_detail.html', {'transaction': transaction})

@login_required
def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    
    if request.method == 'POST':
        transaction.delete()
        messages.success(request, "Transaction deleted successfully.")
        return redirect('dashboard')

    return render(request, 'core/delete_transaction.html', {'transaction': transaction})

@login_required
def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)

    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            messages.success(request, "Transaction updated successfully.")
            return redirect('transaction_detail', pk=transaction.pk)
    else:
        form = TransactionForm(instance=transaction)

    return render(request, 'core/edit_transaction.html', {'form': form, 'transaction': transaction})

@login_required
def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)

    if request.method == 'POST':
        budget.delete()
        messages.success(request, "Budget deleted successfully.")
        return redirect('dashboard')

    return render(request, 'core/delete_budget.html', {'budget': budget})

@login_required
def edit_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)

    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget updated successfully.")
            return redirect('dashboard')
    else:
        form = BudgetForm(instance=budget)

    return render(request, 'core/edit_budget.html', {'form': form, 'budget': budget})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)

    # Check if category is in use
    has_transactions = category.transaction_set.exists()
    has_budgets = category.budget_set.exists()

    if request.method == 'POST':
        if not has_transactions and not has_budgets:
            category.delete()
            messages.success(request, "Category deleted successfully.")
            return redirect('dashboard')
        else:
            messages.error(request, "Cannot delete category in use.")
            return redirect('dashboard')

    return render(request, 'core/delete_category.html', {
        'category': category,
        'has_transactions': has_transactions,
        'has_budgets': has_budgets,
    })

@login_required
def category_manager(request):
    categories = Category.objects.filter(user=request.user)

    # Attach usage flags
    for cat in categories:
        cat.used_in_transactions = cat.transaction_set.exists()
        cat.used_in_budgets = cat.budget_set.exists()

    return render(request, 'core/category_manager.html', {'categories': categories})

@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('category_manager')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'core/edit_category.html', {
        'form': form,
        'category': category
    })

@login_required
def generate_financial_tips(request):
    if request.method == 'GET':
        output = client.models.generate_content(model="gemini-2.0-flash",contents="Provide a one to two sentence personal finance tip. Try not to make it too basic and be intriguing.")
        print(output)
        text_output = output.text
        print(text_output)
        return JsonResponse({'text': text_output})

def financial_report(request):
    categories = Category.objects.all()
    report_data = []

    for category in categories:
        income = Transaction.objects.filter(user=request.user, category=category, type='income').aggregate(total=Sum('amount'))['total'] or 0
        expenses = Transaction.objects.filter(user=request.user, category=category, type='expense').aggregate(total=Sum('amount'))['total'] or 0
        budget = Budget.objects.filter(category=category).first()

        if budget:
            over_budget = expenses > budget.amount
        else:
            over_budget = None  # No budget set

        report_data.append({
            'category': category.name,
            'income': income,
            'expenses': expenses,
            'budget': budget.amount if budget else "No budget set",
            'over_budget': over_budget,
        })

    context = {
        'report_data': report_data
    }
    return render(request, 'core/financial_report.html', context)