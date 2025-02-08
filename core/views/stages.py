from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import ModelForm
from core.models import Stage, Competition, CustomUser
from django import forms

class StageForm(ModelForm):
    judges_ids = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '3',
            'placeholder': 'Введите ID судей, каждый с новой строки'
        }),
        label='Судьи (ID)'
    )
    marshals_ids = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '3',
            'placeholder': 'Введите ID маршалов, каждый с новой строки'
        }),
        label='Маршалы (ID)'
    )
    commentators_ids = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '3',
            'placeholder': 'Введите ID комментаторов, каждый с новой строки'
        }),
        label='Комментаторы (ID)'
    )
    streamers_ids = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': '3',
            'placeholder': 'Введите ID стримеров, каждый с новой строки'
        }),
        label='Стримеры (ID)'
    )

    class Meta:
        model = Stage
        fields = [
            'name', 'track_name', 'track_link', 'technical_regulations',
            'tech_reg_file', 'judging_criteria', 'video_link',
            'registration_slots', 'registration_start', 'registration_end',
            'qualification_start', 'battles_start'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название этапа'
            }),
            'track_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название трассы'
            }),
            'track_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            }),
            'technical_regulations': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Введите технический регламент'
            }),
            'tech_reg_file': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'judging_criteria': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'video_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://'
            }),
            'registration_slots': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'registration_start': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'step': '60'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'registration_end': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'step': '60'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'qualification_start': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'step': '60'
                },
                format='%Y-%m-%dT%H:%M'
            ),
            'battles_start': forms.DateTimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'datetime-local',
                    'step': '60'
                },
                format='%Y-%m-%dT%H:%M'
            ),

        }
        labels = {
            'name': 'Название',
            'track_name': 'Название трассы',
            'track_link': 'Ссылка на трассу',
            'technical_regulations': 'Технический регламент',
            'tech_reg_file': 'Файл технического регламента',
            'judging_criteria': 'Судейское задание',
            'video_link': 'Ссылка на видео',
            'registration_slots': 'Количество слотов (0 - без ограничений)',
            'registration_start': 'Начало регистрации',
            'registration_end': 'Окончание регистрации',
            'qualification_start': 'Начало квалификации',
            'battles_start': 'Начало парных заездов'
        }

@login_required
def stage_create(request, comp_id):
    competition = get_object_or_404(Competition, id=comp_id)
    
    if request.user != competition.organization.created_by:
        messages.error(request, 'У вас нет прав для создания этапа в этом соревновании')
        return redirect('competition_detail', comp_id=comp_id)

    if request.method == 'POST':
        form = StageForm(request.POST, request.FILES)
        if form.is_valid():
            stage = form.save(commit=False)
            stage.competition = competition
            stage.save()
            
            # Обрабатываем ID персонала
            def get_users_by_ids(ids_str):
                if not ids_str:
                    return []
                ids = [id.strip() for id in ids_str.split('\n') if id.strip()]
                return list(CustomUser.objects.filter(public_id__in=ids))
            
            stage.judges.set(get_users_by_ids(form.cleaned_data['judges_ids']))
            stage.marshals.set(get_users_by_ids(form.cleaned_data['marshals_ids']))
            stage.commentators.set(get_users_by_ids(form.cleaned_data['commentators_ids']))
            stage.streamers.set(get_users_by_ids(form.cleaned_data['streamers_ids']))
            
            messages.success(request, 'Этап успешно создан')
            return redirect('competition_detail', comp_id=comp_id)
    else:
        form = StageForm()

    return render(request, 'stages/create.html', {
        'form': form,
        'competition': competition
    })

@login_required
def stage_detail(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)
    return render(request, 'stages/detail.html', {
        'stage': stage
    })

@login_required
def stage_edit(request, stage_id):
    stage = get_object_or_404(Stage, id=stage_id)
    
    if request.user != stage.competition.organization.created_by:
        messages.error(request, 'У вас нет прав для редактирования этого этапа')
        return redirect('stage_detail', stage_id=stage_id)

    if request.method == 'POST':
        form = StageForm(request.POST, request.FILES, instance=stage)
        if form.is_valid():
            stage = form.save(commit=False)
            
            # Обрабатываем ID персонала
            def get_users_by_ids(ids_str):
                if not ids_str:
                    return []
                ids = [id.strip() for id in ids_str.split('\n') if id.strip()]
                return list(CustomUser.objects.filter(public_id__in=ids))
            
            stage.judges.set(get_users_by_ids(form.cleaned_data['judges_ids']))
            stage.marshals.set(get_users_by_ids(form.cleaned_data['marshals_ids']))
            stage.commentators.set(get_users_by_ids(form.cleaned_data['commentators_ids']))
            stage.streamers.set(get_users_by_ids(form.cleaned_data['streamers_ids']))
            
            stage.save()
            messages.success(request, 'Этап успешно обновлен')
            return redirect('stage_detail', stage_id=stage_id)
    else:
        form = StageForm(instance=stage)
        
        # Заполняем поля ID персонала
        form.initial['judges_ids'] = '\n'.join(user.public_id for user in stage.judges.all())
        form.initial['marshals_ids'] = '\n'.join(user.public_id for user in stage.marshals.all())
        form.initial['commentators_ids'] = '\n'.join(user.public_id for user in stage.commentators.all())
        form.initial['streamers_ids'] = '\n'.join(user.public_id for user in stage.streamers.all())

    return render(request, 'stages/edit.html', {
        'form': form,
        'stage': stage
    })
