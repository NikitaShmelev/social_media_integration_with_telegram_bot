# Generated by Django 3.0.4 on 2020-03-31 13:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_1', models.TextField(verbose_name='media_1')),
                ('media_2', models.TextField(verbose_name='media_2')),
                ('media_3', models.TextField(verbose_name='media_3')),
                ('media_4', models.TextField(verbose_name='media_4')),
                ('media_5', models.TextField(verbose_name='media_5')),
                ('media_6', models.TextField(verbose_name='media_6')),
                ('media_7', models.TextField(verbose_name='media_7')),
                ('media_8', models.TextField(verbose_name='media_8')),
                ('media_9', models.TextField(verbose_name='media_9')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.Post', verbose_name='Post')),
            ],
        ),
    ]
