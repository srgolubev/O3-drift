from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def organization_create(request):
    # Пока заглушка: можно будет добавить форму для создания организации
    return render(request, 'core/organization_create.html')
