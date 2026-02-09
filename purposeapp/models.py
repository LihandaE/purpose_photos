# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField('profile_pics', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = CloudinaryField('photos')
    title = models.CharField(max_length=200)
    tags = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.filter(value=1).count()

    def total_dislikes(self):
        return self.likes.filter(value=-1).count()

    def __str__(self):
        return self.title

class Like(models.Model):
    LIKE_CHOICES = (
        (1, 'Like'),
        (-1, 'Dislike'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, related_name='likes', on_delete=models.CASCADE)
    value = models.IntegerField(choices=LIKE_CHOICES)

    class Meta:
        unique_together = ('user', 'photo')

