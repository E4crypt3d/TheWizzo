# Generated by Django 4.1.5 on 2023-02-07 13:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('usertimeline', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='likedcomment', to=settings.AUTH_USER_MODEL),
        ),
    ]
