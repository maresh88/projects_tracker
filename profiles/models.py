from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Profile(MPTTModel):
    """ This model represents the relation between a manager and his/her reporters using mptt library """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports')

    class MPTTMeta:
        order_insertion_by = ['user']

    def __str__(self):
        return f'{self.user}'


@receiver(models.signals.post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    """ Bind Profile and User objects"""
    if created and (not instance.is_superuser or not instance.is_staff):
        Profile.objects.create(user=instance)
