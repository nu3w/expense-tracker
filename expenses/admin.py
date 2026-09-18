from django.contrib import admin
from .models import Category, Expense

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
admin.site.register(Category, CategoryAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'user']
admin.site.register(Expense, ExpenseAdmin)