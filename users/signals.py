from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from users.models import User, Profile
from PIL import Image
from django.core.files.base import ContentFile
import io


@receiver(post_save, sender=User)
def set_user_profile(sender, instance, **kwargs):
    profile, create_profile = Profile.objects.get_or_create(user=instance)
    default_profile_pic = {
        'Male': 'profile_pics/wizzo-default-male-profile.png',
        'Female': 'profile_pics/wizzo-default-female-profile.png',
        'Custom': 'profile_pics/wizzo-default-custom-profile.png'
    }
    if create_profile:
        if instance.gender == 'Male':
            profile.profile_pic = default_profile_pic['Male']
        elif instance.gender == 'Custom':
            profile.profile_pic = default_profile_pic['Custom']
        elif instance.gender == 'Female':
            profile.profile_pic = default_profile_pic['Female']
        else:
            profile.profile_pic = default_profile_pic['Custom']
        profile.save()


@receiver(pre_save, sender=Profile)
def resize_user_profile_pic(sender, instance, **kwargs):
    default_profile_pic = ['profile_pics/wizzo-default-male-profile.png',
                           'profile_pics/wizzo-default-custom-profile.png',
                           'profile_pics/wizzo-default-female-profile.png']
    print(kwargs)
    print(instance.profile_pic, 'newpath')
    # print(instance.profile_pic.path, 'path')
    print(sender)
    if instance.profile_pic in default_profile_pic:
        image = Image.open(instance.profile_pic)
        print(image.size, 'this is the size')

        # Set the desired maximum size of the thumbnail
        if instance.profile_pic and instance.profile_pic not in default_profile_pic:
            max_size = (400, 400)

            # Create a thumbnail with the desired maximum size
            image.thumbnail(max_size)
            resized_image_io = io.BytesIO()
            image.save(resized_image_io, format='JPEG')
            instance.profile_pic.save(instance.profile_pic.name, ContentFile(
                resized_image_io.getvalue()), save=False)

        # Save the thumbnail to a file

    else:
        print('in default')
