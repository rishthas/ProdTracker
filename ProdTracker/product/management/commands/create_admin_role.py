from django.core.management.base import BaseCommand, CommandError
from django.utils.translation import ugettext_lazy as _
from accounts.models import Role,RoleAccess,Profile
from django.contrib.auth.models import User
from django.conf import settings


class Command(BaseCommand):
    def menu_access_for_admin(self,role,menu_array):
        for menu in menu_array:
            if "submenu" in menu:
                role_access, created = RoleAccess.objects.get_or_create(role=role,access_point=menu['ref'],access_string='child')
                role_access.save()
                self.menu_access_for_admin(role,menu["submenu"])
            else:
                for access_type in menu["access_type"]:
                    role_access, created = RoleAccess.objects.get_or_create(role=role,access_point=menu['ref'],access_string=access_type['type'])
                    role_access.save()

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(_('Starting Admin Role and Assign to the admin user') ))
        if hasattr(settings,'ADMIN_MENU'):
            if User.objects.filter(id=1):
                self.stdout.write(self.style.NOTICE(_('Admin User available') ))
                admin_role ,created = Role.objects.get_or_create(role_id='Admin',description='Admin')
                admin_role.save()
                menuArray = settings.ADMIN_MENU
                self.stdout.write("Generating Menu for Admin")
                self.menu_access_for_admin(admin_role,menuArray)
                admin_profile = Profile.objects.get(user__id=1)
                admin_profile.role_id = admin_role
                admin_profile.save()


            else:
                self.stdout.write(self.style.WARNING(_('Admin User Not available') ))
        else:
            self.stdout.write(self.style.WARNING(_('Menu JSON is present in the setting.py') ))


