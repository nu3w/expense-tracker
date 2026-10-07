from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense, Category
from .forms import ExpenseForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum, Avg
from datetime import date
from django.db.models.functions import TruncMonth

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user)
    
    # Count the number of expenses
    total_expenses = expenses.count()
    
    # Get the 4 most recent expenses
    recent_expenses = expenses.order_by(
        '-date',
        '-id'
    )[:4]
    
    # Calculate the total amount spent
    total_amount = expenses.aggregate(
        total = Sum('amount')
    )['total'] or 0
    
    # Calculate the average expense
    average_amount = expenses.aggregate(
        average = Avg('amount')
    )['average'] or 0
    
    # Calculate spending for each category
    category_totals = (
        expenses 
        .values('category__name')
        .annotate(
            total=Sum('amount')
        )
        .order_by('-total')
    )
    
    # Convert category data into a simple list that JavaScript can understand
    chart_data = []
    
    for category in category_totals:
        chart_data.append({
            'category': category['category__name'],
            'total': float(category['total']),
        })
    
    # Get today's date
    today = date.today()
    
    # Get the current year
    current_year = today.year
    
    # Get the current month
    current_month = today.month
    
    # Calculate this month's spending
    this_month_amount = expenses.filter(
        date__year = current_year,
        date__month = current_month
    ).aggregate(
        total = Sum('amount')
    )['total'] or 0
    
    # Calculate the previous month's speending
    if current_month == 1:
        
        previous_month = 12
        previous_year = current_year - 1
        
    else:
        previous_month = current_month - 1
        previous_year = current_year
        
    # Calculate last month's spending
    last_month_amount = expenses.filter(
        date__year = previous_year,
        date__month = previous_month
    ).aggregate(
        total = Sum('amount')
    )['total'] or 0
        
    # Send the statistics to the dashboard template
    return render(request, 'expenses/dashboard.html', {
        'total_expenses': total_expenses,
        'total_amount': total_amount,
        'average_amount': average_amount,
        'category_totals': category_totals,
        'this_month_amount': this_month_amount,
        'last_month_amount': last_month_amount,
        'chart_data': chart_data,
        'recent_expenses': recent_expenses,
    })

@login_required
def expense_list(request):
    # Get only the logged-in user's expenses
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    # Get the serch texy from the URL
    search = request.GET.get('search')
    
    # Get the selected category from the URL
    category_id = request.GET.get('category')
    
    # Get starting date from the URL
    date_from = request.GET.get('date_from')
    
    # Get ending date from the URL
    date_to = request.GET.get('date_to')
    
    # Get the sorting option from the URL
    sort = request.GET.get('sort')
    
    # Sort expenses
    if sort == 'oldest':
        expenses = expenses.order_by('date')
        
    elif sort == 'amount_high':
        expenses = expenses.order_by('-amount')
        
    elif sort == 'amount_low':
        expenses = expenses.order_by('amount')
        
    else:
        expenses = expenses.order_by('-date')
    
    # If the user entered a search term
    if search:
        # Search for expenses whose title contains the text
        expenses = expenses.filter(title__icontains=search)

    # If the user selected a category
    if category_id:
        # Filter expenses by that category
        expenses = expenses.filter(category_id=category_id)
        
    # Filter expenses from this data onwards
    if date_from:
        expenses = expenses.filter(date__gte=date_from)
        
    # Filter expenses up to this date
    if date_to:
        expenses = expenses.filter(date__lte=date_to)
        
    paginator = Paginator(expenses, 10)
    
    # Get the page number from the URL
    page_number = request.GET.get('page')
        
    # Get the requested page
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for the dropdown
    categories = Category.objects.all()
    
    return render(request, 'expenses/expense_list.html', {
        'page_obj': page_obj,
        'expenses': page_obj,
        'categories': categories,
        'search': search,
        'selected_category': category_id,
        'date_from': date_from,
        'date_to': date_to,
        'sort': sort,
    })
    
@login_required
def expense_detail(request, id):
    # Find the expense using its ID
    expense = get_object_or_404(
        Expense,
        id=id,
        user = request.user
    )
    
    # Send the expense to the detail template
    return render(request, 'expenses/expense_detail.html', {
        'expense': expense
    })

@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            
            return redirect('expense_list')
        
    else:
        form = ExpenseForm()
        
    return render(request, 'expenses/expense_create.html', {'form': form})

@login_required
def expense_update(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('expense_list')
        
    else:
        form = ExpenseForm(instance=expense)
        
    return render(request, 'expenses/expense_create.html', {'form': form, 'title': 'Edit Expense'})

@login_required
def expense_delete(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    
    if request.method =='POST':
        expense.delete()
        
        return redirect('expense_list')
    
    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})