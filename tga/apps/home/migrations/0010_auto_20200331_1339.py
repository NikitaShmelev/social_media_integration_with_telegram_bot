# Generated by Django 3.0.4 on 2020-03-31 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20200331_1338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='channel',
            old_name='user_id',
            new_name='user',
        ),
    ]