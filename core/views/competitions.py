from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm
from core.models import Competition, Organization
from django import forms

def competitions_list(request):
    competitions = Competition.objects.filter(is_active=True).order_by('-start_date')
    return render(request, 'competitions/list.html', {'competitions': competitions})

class CompetitionForm(ModelForm):
    class Meta:
        model = Competition
        fields = ['name', 'platform', 'description', 'rules', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'rules': forms.Textarea(attrs={'rows': 8}),
        }

@login_required
def competition_detail(request, comp_id):
    competition = get_object_or_404(Competition, id=comp_id)
    stages = competition.stages.all()
    return render(request, 'competitions/detail.html', {
        'competition': competition,
        'stages': stages
    })

@login_required
def competition_cancel(request, comp_id):
    competition = get_object_or_404(Competition, id=comp_id)
    
    if request.user != competition.organization.created_by:
        messages.error(request, 'У вас нет прав для отмены этого соревнования')
        return redirect('competition_detail', comp_id=comp_id)

    if request.method == 'POST':
        competition.is_active = False
        competition.save()
        messages.success(request, 'Соревнование отменено')

    return redirect('competition_detail', comp_id=comp_id)

@login_required
def competition_edit(request, comp_id):
    competition = get_object_or_404(Competition, id=comp_id)
    
    if request.user != competition.organization.created_by:
        messages.error(request, 'У вас нет прав для редактирования этого соревнования')
        return redirect('competition_detail', comp_id=comp_id)

    if request.method == 'POST':
        form = CompetitionForm(request.POST, instance=competition)
        if form.is_valid():
            form.save()
            messages.success(request, 'Соревнование успешно обновлено')
            return redirect('competition_detail', comp_id=comp_id)
    else:
        form = CompetitionForm(instance=competition)

    return render(request, 'competitions/edit.html', {
        'form': form,
        'competition': competition
    })

@login_required
def competition_create(request, org_id):
    organization = get_object_or_404(Organization, id=org_id)
    
    if request.user != organization.created_by:
        messages.error(request, 'У вас нет прав для создания соревнования в этой организации')
        return redirect('organization_detail', org_id=org_id)

    if request.method == 'POST':
        form = CompetitionForm(request.POST)
        if form.is_valid():
            competition = form.save(commit=False)
            competition.organization = organization
            competition.save()
            messages.success(request, 'Соревнование успешно создано')
            return redirect('organization_detail', org_id=org_id)
    else:
        form = CompetitionForm()

    return render(request, 'competitions/create.html', {
        'form': form,
        'organization': organization
    })
