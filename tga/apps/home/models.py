from django.db import models

# Create your models here.


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
        return f'#{self.email} {self.username}'


class Channel(models.Model):

    user = models.ForeignKey(
        to='home.UserProfile',
        verbose_name='User ID',
        on_delete=models.PROTECT,
    )
    
    channel_id = models.PositiveIntegerField(
        verbose_name='Channel ID',
    )
    

class Post(models.Model):
    user = models.ForeignKey(
        to='home.UserProfile',
        verbose_name='User Profile',
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(
        verbose_name='Creation time',
    )   
    post_text = models.TextField(
        verbose_name='post_text',
    )
    creator_name = models.TextField(
        verbose_name='creator_name',
    )
    media = models.BooleanField(
        verbose_name='media',
    )
    location = models.BooleanField(
        verbose_name='location',
    )
    published = models.BooleanField(
        verbose_name='published',
    )


class PostMedia(models.Model):
    post = models.ForeignKey(
        to='home.Post',
        verbose_name='Post',
        on_delete=models.PROTECT,
    )
    media_1 = models.TextField(
        verbose_name='media_1',
    )
    media_2 = models.TextField(
        verbose_name='media_2',
    )
    media_3 = models.TextField(
        verbose_name='media_3',
    )
    media_4 = models.TextField(
        verbose_name='media_4',
    )
    media_5 = models.TextField(
        verbose_name='media_5',
    )
    media_6 = models.TextField(
        verbose_name='media_6',
    )
    media_7 = models.TextField(
        verbose_name='media_7',
    )
    media_8 = models.TextField(
        verbose_name='media_8',
    )
    media_9 = models.TextField(
        verbose_name='media_9',
    )

    class Meta:
        verbose_name = 'Post Media'
        verbose_name_plural = 'Post Media'


class PostLocation(models.Model):
    post = models.ForeignKey(
        to='home.Post',
        verbose_name='Post',
        on_delete=models.PROTECT,
    )
    latitude = models.TextField(
        verbose_name='latitude',
    )
    longitude = models.TextField(
        verbose_name='longitude',
    )
    class Meta:
        verbose_name = 'Post Location'
        verbose_name_plural = 'Post Location'
    


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