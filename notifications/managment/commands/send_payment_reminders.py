# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from datetime import timedelta
# from django.core.mail import send_mail
# from payment.models import Payment

# class Command(BaseCommand):
#     help = 'Send payment reminder emails for subscriptions expiring in 5 days'
#     def handle(self, *args, **options):
    
#         today = timezone.now().date()
#         target_day = today + timedelta(days=5)

#         payments = Payment.objects.filter(end_date=target_day, reminder_sent=False)

#         for payment in payments:
#             try:
#                 send_mail(
#                     subject="Your subscription is about to expire",
#                     message=(
#                         f"Dear {payment.customer.first_name} {payment.customer.last_name},\n\n"
#                         "Your subscription will expire in 5 days.\n"
#                         "Please renew to avoid interruption.\n\n"
#                         "Thank you.\n"
#                         "Sunshine Bole Beshale House Owners Association"
#                     ),
#                     from_email="learndjango4444@gmail.com",
#                     recipient_list=[payment.customer.email],
#                     fail_silently=False,
#                 )
#                 payment.reminder_sent = True
#                 payment.save()

#             except Exception as e:
#                 self.stderr.write(
#                     self.style.ERROR(
#                         f'Failed for {payment.customer.email}: {str(e)}'
#                     )
#                 )
#         self.stdout.write(self.style.SUCCESS("Reminder emails sent successfully"))
