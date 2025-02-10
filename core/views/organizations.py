from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm
from django.core.exceptions import PermissionDenied
from core.models import Organization

def organizations_list(request):
    organizations = Organization.objects.all().order_by('name')
    return render(request, 'organizations/list.html', {'organizations': organizations})

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = ['name', 'abbreviation', 'description', 'logo']
        labels = {
            'name': 'Название организации',
            'abbreviation': 'Аббревиатура',
            'description': 'Описание',
            'logo': 'Логотип'
        }

@login_required
def organization_create(request):
    if not request.user.profile.is_organizer:
        messages.error(request, 'У вас нет прав для создания организации')
        return redirect('profile')

    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            organization = form.save(commit=False)
            organization.created_by = request.user
            organization.save()
            messages.success(request, 'Организация успешно создана')
            return redirect('profile')
    else:
        form = OrganizationForm()

    return render(request, 'organizations/create.html', {'form': form})

@login_required
def organization_detail(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    competitions = organization.competitions.filter(is_active=True)
    
    return render(request, 'organizations/detail.html', {
        'organization': organization,
        'competitions': competitions,
    })

@login_required
def organization_edit(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    
    if request.user != organization.created_by:
        messages.error(request, 'У вас нет прав для редактирования этой организации')
        return redirect('organization_detail', org_id=org_id)

    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES, instance=organization)
        if form.is_valid():
            form.save()
            messages.success(request, 'Организация успешно обновлена')
            return redirect('organization_detail', org_id=org_id)
    else:
        form = OrganizationForm(instance=organization)

    return render(request, 'organizations/edit.html', {
        'form': form,
        'organization': organization
    })
