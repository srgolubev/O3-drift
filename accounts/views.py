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
    is_organizer = request.user.groups.filter(name='Organizers').exists()
    organizations = []
    if is_organizer:
        from core.models import Organization
        organizations = Organization.objects.filter(created_by=request.user)
    return render(request, 'accounts/profile.html', {'organizations': organizations, 'is_organizer': is_organizer})

# --- Begin profile_edit view ---
@login_required
def profile_edit(request):
    from .forms import UserProfileForm
    from django.shortcuts import redirect
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'accounts/profile_edit.html', {'form': form})
# --- End profile_edit view ---
