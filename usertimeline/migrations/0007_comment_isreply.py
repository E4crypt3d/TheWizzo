# Generated by Django 4.1.5 on 2023-02-08 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usertimeline', '0006_alter_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='isreply',
            field=models.BooleanField(default=False),
        ),
    ]
