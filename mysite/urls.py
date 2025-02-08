"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from core.views.organizations import organizations_list, organization_create, organization_detail, organization_edit
from core.views.competitions import competitions_list, competition_create, competition_detail, competition_edit, competition_cancel
from core.views.stages import stage_create, stage_detail, stage_edit

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('core.api.urls')),
    path('accounts/', include('accounts.urls')),
    path('organizations/', organizations_list, name='organizations'),
    path('organizations/create/', organization_create, name='organization_create'),
    path('organizations/<int:org_id>/', organization_detail, name='organization_detail'),
    path('organizations/<int:org_id>/edit/', organization_edit, name='organization_edit'),
    path('competitions/', competitions_list, name='competitions'),
    path('organizations/<int:org_id>/competitions/create/', competition_create, name='competition_create'),
    path('competitions/<int:comp_id>/', competition_detail, name='competition_detail'),
    path('competitions/<int:comp_id>/edit/', competition_edit, name='competition_edit'),
    path('competitions/<int:comp_id>/cancel/', competition_cancel, name='competition_cancel'),
    path('competitions/<int:comp_id>/stages/create/', stage_create, name='stage_create'),
    path('stages/<int:stage_id>/', stage_detail, name='stage_detail'),
    path('stages/<int:stage_id>/edit/', stage_edit, name='stage_edit'),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
