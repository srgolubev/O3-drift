from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from core.models import Organization


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    organizations = Organization.objects.filter(created_by=request.user)
    return render(request, 'accounts/profile.html', {'organizations': organizations})

# --- Begin profile_edit view ---
@login_required
def profile_edit(request):
    from .forms import CustomUserForm, ProfileEditForm
    from django.shortcuts import redirect, render
    user = request.user
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = CustomUserForm(instance=user)
        profile_form = ProfileEditForm(instance=user.profile)
    return render(request, 'accounts/profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})
# --- End profile_edit view ---
