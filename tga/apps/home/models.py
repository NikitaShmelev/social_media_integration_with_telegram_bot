from django.db import models

# Create your models here.


class Post(models.Model):
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
    