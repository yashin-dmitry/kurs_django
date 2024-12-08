from django.db import models
from users.models import CustomUser

class Client(models.Model):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        permissions = [
            ("custom_view_client", "Can view client"),
        ]

    def __str__(self):
        return self.email

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()

    class Meta:
        permissions = [
            ("custom_view_message", "Can view message"),
        ]

    def __str__(self):
        return self.subject

class Mailing(models.Model):
    STATUS_CHOICES = [
        ('Завершена', 'Завершена'),
        ('Создана', 'Создана'),
        ('Запущена', 'Запущена'),
    ]

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    clients = models.ManyToManyField(Client)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ("custom_view_mailing", "Can view mailing"),
        ]

    def __str__(self):
        return f"Mailing {self.id} - {self.status}"

class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('Успешно', 'Успешно'),
        ('Не успешно', 'Не успешно'),
    ]

    attempt_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    server_response = models.TextField(blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)

    def __str__(self):
        return f"Attempt {self.id} - {self.status}"
