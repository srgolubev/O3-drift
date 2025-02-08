from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import utils as django_db_utils
from decimal import Decimal
from datetime import date, datetime, timezone
from core.models import (
    Organization, Competition, Profile, Stage,
    QualificationResult, BattleBracket, Battle, BattleRun
)

User = get_user_model()


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
        cls.user = User.objects.create_user(username='testuser', password='testpass', email='test@example.com')
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


class StageTestCase(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Test Organization')
        self.comp = Competition.objects.create(
            name='Test Competition',
            organization=self.org,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31)
        )
        self.stage = Stage.objects.create(
            competition=self.comp,
            name='Test Stage',
            track_name='Test Track'
        )
        self.user1 = User.objects.create_user(username='user1', password='pass1', email='user1@example.com')
        self.user2 = User.objects.create_user(username='user2', password='pass2', email='user2@example.com')

    def test_stage_str(self):
        self.assertEqual(str(self.stage), 'Test Competition - Test Stage')

    def test_stage_roles(self):
        # Проверяем добавление ролей
        self.stage.judges.add(self.user1)
        self.stage.marshals.add(self.user2)
        
        self.assertIn(self.user1, self.stage.judges.all())
        self.assertIn(self.user2, self.stage.marshals.all())


class QualificationResultTestCase(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Test Organization')
        self.comp = Competition.objects.create(
            name='Test Competition',
            organization=self.org,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31)
        )
        self.stage = Stage.objects.create(
            competition=self.comp,
            name='Test Stage'
        )
        self.user = User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')

    def test_qualification_result_creation(self):
        result = QualificationResult.objects.create(
            stage=self.stage,
            participant=self.user,
            attempt_number=1,
            score=Decimal('95.5'),
            angle_score=Decimal('28.5'),
            line_score=Decimal('27.0'),
            style_score=Decimal('20.0'),
            speed_score=Decimal('20.0')
        )
        self.assertEqual(result.score, Decimal('95.5'))
        self.assertEqual(result.attempt_number, 1)

    def test_unique_attempt_constraint(self):
        # Проверяем ограничение на уникальность попытки
        QualificationResult.objects.create(
            stage=self.stage,
            participant=self.user,
            attempt_number=1,
            score=Decimal('95.5')
        )
        with self.assertRaises(django_db_utils.IntegrityError):
            QualificationResult.objects.create(
                stage=self.stage,
                participant=self.user,
                attempt_number=1,
                score=Decimal('90.0')
            )


class BattleTestCase(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name='Test Organization')
        self.comp = Competition.objects.create(
            name='Test Competition',
            organization=self.org,
            start_date=date(2025, 1, 1),
            end_date=date(2025, 1, 31)
        )
        self.stage = Stage.objects.create(
            competition=self.comp,
            name='Test Stage'
        )
        self.bracket = BattleBracket.objects.create(
            stage=self.stage,
            bracket_type='TOP_32'
        )
        self.user1 = User.objects.create_user(username='driver1', password='pass1', email='driver1@example.com')
        self.user2 = User.objects.create_user(username='driver2', password='pass2', email='driver2@example.com')

    def test_battle_creation(self):
        battle = Battle.objects.create(
            bracket=self.bracket,
            leader=self.user1,
            follower=self.user2,
            battle_order=1
        )
        self.assertEqual(battle.state, 'PENDING')
        self.assertIsNone(battle.winner)

    def test_battle_run_scores(self):
        battle = Battle.objects.create(
            bracket=self.bracket,
            leader=self.user1,
            follower=self.user2,
            battle_order=1
        )
        
        # Создаем заезды
        lead_run = BattleRun.objects.create(
            battle=battle,
            run_type='LEAD',
            driver=self.user1,
            angle_score=Decimal('28.5'),
            line_score=Decimal('27.0'),
            style_score=Decimal('20.0'),
            speed_score=Decimal('20.0'),
            total_score=Decimal('95.5')
        )
        follow_run = BattleRun.objects.create(
            battle=battle,
            run_type='FOLLOW',
            driver=self.user2,
            angle_score=Decimal('27.0'),
            line_score=Decimal('26.5'),
            style_score=Decimal('19.5'),
            speed_score=Decimal('19.0'),
            total_score=Decimal('92.0')
        )

        self.assertEqual(lead_run.total_score, Decimal('95.5'))
        self.assertEqual(follow_run.total_score, Decimal('92.0'))

    def test_unique_run_type_constraint(self):
        battle = Battle.objects.create(
            bracket=self.bracket,
            leader=self.user1,
            follower=self.user2,
            battle_order=1
        )
        
        BattleRun.objects.create(
            battle=battle,
            run_type='LEAD',
            driver=self.user1,
            total_score=Decimal('95.5')
        )
        
        # Проверяем, что нельзя создать второй LEAD заезд
        with self.assertRaises(django_db_utils.IntegrityError):
            BattleRun.objects.create(
                battle=battle,
                run_type='LEAD',
                driver=self.user2,
                total_score=Decimal('92.0')
            )
