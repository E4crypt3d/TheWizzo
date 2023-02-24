from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import User, Profile


@receiver(post_save, sender=User)
def set_user_profile(sender, instance, **kwargs):
    profile, create_profile = Profile.objects.get_or_create(user=instance)
    if instance.gender == 'Male':
        profile.profile_pic = 'profile_pics/wizzo-default-male-profile.png'
    elif instance.gender == 'Custom':
        profile.profile_pic = 'profile_pics/wizzo-default-custom-profile.png'
    elif instance.gender == 'Female':
        profile.profile_pic = 'profile_pics/wizzo-default-female-profile.png'
    else:
        profile.profile_pic = 'profile_pics/wizzo-default-custom-profile.png'
    profile.save()
