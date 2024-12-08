from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from mailings.models import Client, Message, Mailing

class Command(BaseCommand):
    help = 'Create manager group with necessary permissions'

    def handle(self, *args, **kwargs):
        manager_group, created = Group.objects.get_or_create(name='Менеджеры')
        manager_permissions = Permission.objects.filter(
            content_type__in=ContentType.objects.get_for_models(Client, Message, Mailing).values(),
            codename__in=['custom_view_client', 'custom_view_message', 'custom_view_mailing']
        )
        manager_group.permissions.set(manager_permissions)
        self.stdout.write(self.style.SUCCESS('Manager group created with necessary permissions'))
