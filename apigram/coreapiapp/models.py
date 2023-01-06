from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db.models.signals import post_save

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.


class CoreApiBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Account(CoreApiBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')

    def __str__(self) -> str:
        return self.user.__str__()




class Post(CoreApiBaseModel):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self) -> str:
        return '[{}] {}: {}'.format(self.pk, self.author, self.description)

    @property
    def owner(self) -> User:
        return self.author.user



class PostPhoto(CoreApiBaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_photos', null=True )
    photo = ProcessedImageField(
        upload_to='post_photos',
        processors=[ResizeToFill(1440, 1440)],
        format='JPEG',
        options={'quality': 80},
        unique=True,
        
    )

    author = models.ForeignKey(Account, on_delete=models.CASCADE)

    @property
    def owner(self) -> User:
        return self.author.user

    def __str__(self) -> str:
        
        return '[{}] {}'.format(self.post, self.photo.name)



def save_account(sender, instance, **kwargs):
    if kwargs['created']:
        Account(user=instance).save()


post_save.connect(save_account, sender=User)