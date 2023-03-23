from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Post, Notification
from PIL import Image
import io
from django.core.files.base import ContentFile


@receiver(pre_save, sender=Post)
def resize_post_image(sender, instance, **kwargs):
    if instance.image:
        uploaded_image = Image.open(instance.image)
        img_size = 800, 600
        uploaded_image.thumbnail(img_size)

        # Get the new size of the image
    new_width, new_height = uploaded_image.size

    # Check if the image needs to be cropped to a square aspect ratio
    if new_width != new_height:
        # Calculate the new dimensions of the image to match the square aspect ratio
        if new_width > new_height:
            new_width = new_height
        else:
            new_height = new_width

        # Crop the image to the new dimensions
        left = int((uploaded_image.width - new_width) / 2)
        top = int((uploaded_image.height - new_height) / 2)
        right = left + new_width
        bottom = top + new_height
        uploaded_image = uploaded_image.crop((left, top, right, bottom))
        temp_image = io.BytesIO()
        uploaded_image.save(temp_image, format="JPEG",
                            optimize=True, quality=100)

        instance.image.save(
            instance.image.name, ContentFile(temp_image.getvalue()), save=False)
#  notification_types = [
#         ('1', 'Follow'),
#         ('2', 'Like'),
#         ('3', 'Comment'),
#         ("4", "Reply"),
#         ("5", "Comment-Like")
#     ]


@receiver(pre_save, sender=Notification)
def handle_notifications(sender, instance, **kwargs):
    if instance.noti_type == "1":
        instance.notification = f"{instance.sender} just started following you!"
    elif instance.noti_type == "2":
        instance.notification = f"{instance.sender} liked your post."
    elif instance.noti_type == "3":
        instance.notification = f"{instance.sender} commented on your post. '{instance.post.caption[:20]}'"
