from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToCover

# Create your models here.


class CoreApiBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Account(CoreApiBaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='account')

    def __str__(self) -> str:
        return self.user.__str__()


class AccountPhoto(CoreApiBaseModel):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, related_name='account_photo', null=True)

    photo = ProcessedImageField(
        upload_to='account_photos',
        processors=[ResizeToCover(512, 512)],
        format='JPEG',
        default='account_photos/default.jpg',
    )

    photo_thumbnail = ImageSpecField(
        source='photo',
        format='JPEG',
        processors=[
            ResizeToCover(128, 128)
        ],
    )

    def __str__(self) -> str:
        return '[{}] {}'.format(self.account, self.photo.name)

    @property
    def owner(self) -> User:
        return self.account.user


class Post(CoreApiBaseModel):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self) -> str:
        return '[{}] {}: {}'.format(self.pk, self.author, self.description)

    @property
    def owner(self) -> User:
        return self.author.user


class PostPhoto(CoreApiBaseModel):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='post_photos', null=True)
    photo = ProcessedImageField(
        upload_to='post_photos',
        processors=[ResizeToCover(1440, 1440)],
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
        account = Account(user=instance)
        account.save()
        AccountPhoto(account=account).save()


post_save.connect(save_account, sender=User)
