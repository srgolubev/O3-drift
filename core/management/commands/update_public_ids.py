from django.core.management.base import BaseCommand
from core.models import CustomUser
import random
import string

class Command(BaseCommand):
    help = 'Updates public_ids for all users to new 8-character format'

    def handle(self, *args, **options):
        users = CustomUser.objects.all()
        total = users.count()
        updated = 0

        self.stdout.write(f"Found {total} users to update")

        for user in users:
            while True:
                public_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
                if not CustomUser.objects.filter(public_id=public_id).exists():
                    user.public_id = public_id
                    user.save()
                    updated += 1
                    self.stdout.write(f"Updated {updated}/{total} users", ending='\r')
                    break

        self.stdout.write(self.style.SUCCESS(f"\nSuccessfully updated {updated} users"))
