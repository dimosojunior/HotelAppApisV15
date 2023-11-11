# YourApp/management/commands/delete_inactive_users.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from HotelApis.models import *  # Replace YourApp with your app name
from django.conf import settings
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Deletes users whose registration time exceeds 1 days'

    def handle(self, *args, **options):
        threshold_date = timezone.now() - timezone.timedelta(days=1)
        expired_users = MyUser.objects.filter(date_joined__lt=threshold_date)

        for user in expired_users:
        	

            # Send an email to the user
            subject = 'Registration Expiry'
            message = 'Your registration period has expired. Your account has been deleted.'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        # Delete the expired users
        deleted_users = expired_users.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_users[0]} users.'))
