from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Expense, Category

class ExpenseSecurityTest(TestCase):
    def setUp(self):
        # Create the first user
        self.user1 = User.objects.create_user(
            username='user1',
            password='password123'
        )
        
        # Create the seconf user
        self.user2 = User.objects.create_user(
            username='user2',
            password='password123'
        )
        
        # Create a category
        self.category = Category.objects.create(
            name='Food',
        )
        
        self.expense = Expense.objects.create(
            user=self.user1,
            title='Lunch',
            amount=500,
            category=self.category,
            date='2026-09-20'
        )
        
    def test_user_cannot_edit_another_users_expense(self):
        # Log in as user2
        self.client.login(
            username='user2',
            password='password123'
        )
        
        # Try to access user1's edit
        response = self.client.get(
            reverse(
                'expense_update',
                args=[self.expense.id]
            )
        )
        
        # The page should return 404
        self.assertEqual(
            response.status_code,
            404
        )
        
    def test_user_cannot_delete_another_users_expense(self):
        # Log in as user2
        self.client.login(
            username='user2',
            password='password123'
        )
        
        # Try to access user1's delete page
        response = self.client.get(
            reverse(
                'expense_delete',
                args=[self.expense.id]
            )
        )
        
        # The page should return 404
        self.assertEqual(
            response.status_code,
            404
        )
        
    def test_user_cannot_view_another_users_expense(self):
        # Log in as user2
        self.client.login(
            username='user2',
            password='password123'
        )
        
        # Try to view user1's expense
        response = self.client.get(
            reverse(
                'expense_detail',
                args=[self.expense.id]
            )
        )
        
        # The page should return 404
        self.assertEqual(
            response.status_code,
            404
        )
        
    def test_user_sees_only_their_own_expenses(self):
        # Log in as user1
        self.client.login(
            username='user1',
            password='password123'
        )
        
        # Create another expense belonging to user2
        other_expense = Expense.objects.create(
            user = self.user2,
            title = 'Other User Lunch',
            amount = 300,
            category = self.category,
            date = '2026-09-21'
        )
        
        # Open the expense list
        response = self.client.get(
            reverse('expense_list')
        )
        
        # Check that user1's expense appears
        self.assertContains(
            response,
            'Lunch'
        )
        
        # Check that user2's expense does not appear
        self.assertNotContains(
            response,
            'Other User Lunch'
        )
        
    def test_unauthenticated_user_is_redirected_from_expense_list(self):
        # Open the expense list without logging in
        response = self.client.get(
            reverse('expense_list')
        )
        
        # Display the status code and redirect URL
        print('Status code:', response.status_code)
        print('Redirect URL:', response.url)
        
        # The user should be redirected to the login page
        self.assertEqual(
            response.status_code,
            302
        )
        
        # Check that the redirect goes to the login page
        # self.assertRedirects(
        #     response,
        #     '/users/login/?next=/expenses/'
        # )