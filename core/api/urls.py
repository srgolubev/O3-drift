from django.urls import path
from .views import CompetitionListAPIView, UserProfileAPIView

urlpatterns = [
    path('competitions/', CompetitionListAPIView.as_view(), name='competition-list'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
]
