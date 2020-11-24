from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import user_profile, User


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile.objects.create(userProfile=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.userProfile.save()


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):

    if created == False:
        instance.userProfile.save()

# @receiver(post_save, sender=subarea)
# def create_daily(sender, instance, created, **kwargs):
#     if created:
#         daily.objects.create(dailySubarea=instance)


# @receiver(post_save, sender=subarea)
# def save_daily(sender, instance, **kwargs):
#     instance.daily.save()


# @receiver(post_save, sender=subarea)
# def update_daily(sender, instance, created, **kwargs):

#     if created == False:
#         instance.daily.save()
