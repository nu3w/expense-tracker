from django import forms
from .models import Expense
from datetime import date

class ExpenseForm(forms.ModelForm):
        
    def clean_amount(self):
        # Get the amount entered by the user
        amount = self.cleaned_data['amount']
        
        # Check whether the amount is zero or negative
        if amount <= 0:
            
            # Show an error message
            raise forms.ValidationError(
                'Amount must be greater than zero.'
            )
            
        if amount > 10000000:
            
            raise forms.ValidationError(
                'Amount cannot be greater than 10,000,000.'
            )
            
        # Return the valid amount
        return amount
    
    def clean_title(self):
        # Get the title entered by the user
        title = self.cleaned_data['title']
        
        # Remove spaces from the beginning and the end
        title = title.strip()
        
        # Check whether the title is empty
        if not title:
            raise forms.ValidationError(
                'Title cannot be empty.'
            )
            
        return title
    
    def clean_date(self):
        
        # Get the data entered by the user
        expense_date = self.cleaned_data['date']
        
        # Get today's date
        today = date.today()
        
        # Check whether the expense date is in the future
        if expense_date > today:
            raise forms.ValidationError(
                'Expense date cannot be in the future.'
            )
            
        return expense_date
    
    class Meta:
        model = Expense
        fields = ['title', 'category', 'amount', 'description', 'date']
        
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
        }