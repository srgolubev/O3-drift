from rest_framework import generics, permissions
from core.models import Competition, Profile
from .serializers import CompetitionSerializer, ProfileSerializer


class CompetitionListAPIView(generics.ListAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileAPIView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Возвращает профиль текущего пользователя
        return self.request.user.profile
