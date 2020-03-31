# Generated by Django 3.0.4 on 2020-03-31 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20200331_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(verbose_name='Creation time')),
                ('post_text', models.TextField(verbose_name='post_text')),
                ('creator_name', models.TextField(verbose_name='creator_name')),
                ('media', models.BooleanField(verbose_name='media')),
                ('location', models.BooleanField(verbose_name='location')),
                ('published', models.BooleanField(verbose_name='published')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='home.UserProfile', verbose_name='User Profile')),
            ],
        ),
    ]
