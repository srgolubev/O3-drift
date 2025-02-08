from django.test import TestCase
from django.contrib.auth import get_user_model
User = get_user_model()
from core.models import Organization, Competition, Profile
from datetime import date


class ModelsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org = Organization.objects.create(
            name='Test Organization',
            description='A test organization'
        )
        cls.comp = Competition.objects.create(
            name='Test Competition',
            organization=cls.org,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31),
            description='A test competition'
        )
        cls.user = User.objects.create_user(username='testuser', password='testpass')
        cls.profile, _ = Profile.objects.get_or_create(
            user=cls.user, defaults={'bio': 'This is a test bio'}
        )

    def setUp(self):
        self.org = self.__class__.org
        self.comp = self.__class__.comp
        self.user = self.__class__.user
        self.profile = self.__class__.profile

    def test_organization_str(self):
        self.assertEqual(str(self.org), 'Test Organization')

    def test_competition_str(self):
        self.assertEqual(str(self.comp), 'Test Competition')

    def test_profile_str(self):
        self.assertEqual(str(self.profile), 'testuser')

    def test_relationships(self):
        # Проверяем, что соревнование корректно связано с организацией
        self.assertIn(self.comp, self.org.competitions.all())
