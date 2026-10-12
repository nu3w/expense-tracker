from django.shortcuts import render, redirect
from .forms import RegistrationForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        
    else:
        form = RegistrationForm()
        
    return render(request, 'users/register.html', {'form':form})

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST,
            instance=request.user
        )
        
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Your profile has been updated successfully!'
            )
            
            return redirect('profile')
        
    else:
        form = ProfileUpdateForm(instance=request.user)
        
    return render(
        request,
        'users/edit_profile.html',
        {'form': form}
    )