from django.core.management.base import BaseCommand
from mailings.models import Mailing, MailingAttempt
from django.core.mail import send_mail
from django.utils import timezone

class Command(BaseCommand):
    help = 'Send mailings'

    def handle(self, *args, **kwargs):
        mailings = Mailing.objects.filter(status='Создана', end_time__gte=timezone.now())
        for mailing in mailings:
            for client in mailing.clients.all():
                try:
                    send_mail(
                        mailing.message.subject,
                        mailing.message.body,
                        'from@example.com',
                        [client.email],
                        fail_silently=False,
                    )
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='Успешно',
                        server_response='OK'
                    )
                except Exception as e:
                    MailingAttempt.objects.create(
                        mailing=mailing,
                        status='Не успешно',
                        server_response=str(e)
                    )
            mailing.status = 'Запущена'
            mailing.save()
        self.stdout.write(self.style.SUCCESS('Mailings sent successfully'))
