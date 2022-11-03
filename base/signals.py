from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile, Friend
from django.dispatch import receiver

#-----------------------------------------------------------------------
        
@receiver(post_save, sender=User)
def create_friend(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance, 
            name=instance.username
            )

#-----------------------------------------------------------------------

@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created == False:

        instance.profile.save()

#-----------------------------------------------------------------------

@receiver(post_save, sender=Profile)
def create_friend(sender, instance, created, **kwargs):
    if created:
        Friend.objects.create(
            profile=instance, 
            )