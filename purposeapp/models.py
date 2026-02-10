from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = CloudinaryField(
        'profile_images',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


class Photo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photos')
    image = CloudinaryField('photos')
    title = models.CharField(max_length=200)
    tags = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.like_set.count()

    def total_dislikes(self):
        return self.dislike_set.count()

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'photo')

    def __str__(self):
        return f"{self.user} likes {self.photo}"


class Dislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'photo')

    def __str__(self):
        return f"{self.user} dislikes {self.photo}"
