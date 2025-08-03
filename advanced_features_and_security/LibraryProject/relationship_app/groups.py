# myapp/management/commands/setup_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from myapp.models import Article

class Command(BaseCommand):
    help = 'Set up groups and assign permissions'

    def handle(self, *args, **kwargs):
        content_type = ContentType.objects.get_for_model(Article)

        perms = {
            'can_view': Permission.objects.get(codename='can_view', content_type=content_type),
            'can_create': Permission.objects.get(codename='can_create', content_type=content_type),
            'can_edit': Permission.objects.get(codename='can_edit', content_type=content_type),
            'can_delete': Permission.objects.get(codename='can_delete', content_type=content_type),
        }

        groups_permissions = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }

        for group_name, perm_codenames in groups_permissions.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            for codename in perm_codenames:
                group.permissions.add(perms[codename])

        self.stdout.write(self.style.SUCCESS('Groups and permissions set up successfully.'))
