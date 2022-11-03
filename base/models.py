from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

#-----------------------------------------------------------------------

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    profile_pic = models.ImageField( default='profile-images/default.webp', upload_to='profile-images',blank=True, null=True)
    friends = models.ManyToManyField('Friend', related_name='friends_list', blank='True')
    slug = models.SlugField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None:
             self.slug = slugify(self.name)

        super().save(*args, **kwargs)

#-----------------------------------------------------------------------

class Friend(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.profile.name

    def save(self, *args, **kwargs):
        if self.slug is None:
             self.slug = self.profile.slug
        
        super().save(*args, **kwargs)

#-----------------------------------------------------------------------

class Message(models.Model):
    body = models.TextField()
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body
