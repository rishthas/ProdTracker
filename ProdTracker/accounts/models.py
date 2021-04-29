from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



# Create your models here.

class Role(models.Model):
    role_id = models.CharField(_("Role ID"), max_length=50)
    description = models.CharField(_("Role Description"), max_length=100)

    def __str__(self):
        return self.role_id


    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    role_id = models.ForeignKey(Role, verbose_name=_("Role Id"), on_delete=models.SET_NULL,null=True,blank=True)



    def __str__(self):
        return str(self.user.username)


    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class RoleAccess(models.Model):
    role = models.ForeignKey(Role, verbose_name=_("Role"), on_delete=models.CASCADE,related_name="role_access")
    access_point = models.CharField(_("Access Point"), max_length=50)
    access_string = models.CharField(_("Access Idetifier"), max_length=50)
    

    class Meta:
        verbose_name = _("RoleAccess")
        verbose_name_plural = _("RoleAccesss")

    def __str__(self):
        return '{}_{}_{}'.format(self.role.role_id,self.access_point,self.access_string)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()