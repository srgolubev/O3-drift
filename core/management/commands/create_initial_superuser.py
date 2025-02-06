from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import uuid


class Command(BaseCommand):
    help = 'Creates an initial superuser with preset credentials if it does not exist.'

    def handle(self, *args, **options):
        User = get_user_model()
        username = 'mduck'
        password = 'tibibo@2332'
        email = 'mduck@example.com'
        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
        except User.DoesNotExist:
            # Removed passing public_id since it's auto-generated
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))
