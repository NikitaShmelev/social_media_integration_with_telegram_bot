# Generated by Django 3.0.4 on 2020-03-29 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0002_auto_20200315_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.TextField(default=None, verbose_name='Email'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Message',
        ),
    ]
