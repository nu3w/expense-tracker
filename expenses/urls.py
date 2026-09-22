from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('expenses/add/', views.expense_create, name='expense_create'),
    path('expenses/edit/<int:id>/', views.expense_update, name='expense_update'),
    path('expenses/delete/<int:id>/', views.expense_delete, name='expense_delete'),
    path('expenses/<int:id>/', views.expense_detail, name='expense_detail'),
]
