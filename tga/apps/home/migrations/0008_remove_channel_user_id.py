# Generated by Django 3.0.4 on 2020-03-31 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_channel_user_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='channel',
            name='user_id',
        ),
    ]
