from django.shortcuts import render, redirect
from .forms import RegistrationForm, ProfileUpdateForm, ProfilePictureForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

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
    profile, created = Profile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})

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
    
@login_required
def update_profile_picture(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfilePictureForm(
            request.POST,
            request.FILES,
            instance=profile
        )
        
        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Profile picture updated successfully!'
            )
            
    return redirect('profile')