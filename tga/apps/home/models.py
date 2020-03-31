from django.db import models

# Create your models here.


class Feedback(models.Model):
    email = models.CharField(
        verbose_name='email',
        max_length=50,
        )
    name = models.CharField(
        verbose_name='name',
        max_length=50,
        )
    message = models.TextField(
        verbose_name='message',
    )
    created_at = models.DateTimeField(
        verbose_name='Receive time',
        auto_now_add=True,
    )
    

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user_id = models.PositiveIntegerField(
        verbose_name='User ID',
    )
    username = models.TextField(
        verbose_name='Usename',
    )
    language = models.TextField(
        verbose_name='Selected language',
    )
    email = models.TextField(
        verbose_name='Email',
    )

    def __str__(self):
        return f'#{self.external_id} {self.name}'