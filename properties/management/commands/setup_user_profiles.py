from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from properties.models import UserProfile

User = get_user_model()

class Command(BaseCommand):
    help = 'Sets up UserProfile instances for all users'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        created_count = 0
        
        for user in users:
            profile, created = UserProfile.objects.get_or_create(user=user)
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created profile for user {user.username}'))
        
        self.stdout.write(self.style.SUCCESS(f'Successfully processed {len(users)} users. Created {created_count} new profiles.')) 