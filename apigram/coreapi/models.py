from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class CoreApiBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Account(CoreApiBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.__str__()



class Post(CoreApiBaseModel):
    author = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self) -> str:
        return '[{}] {}: {}'.format(self.pk, self.author, self.description)



class PostPhoto(CoreApiBaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_photos' )
    photo = models.ImageField(upload_to='post_photos')

    def __str__(self) -> str:
        
        return '[{}] {}'.format(self.post, self.photo.name)
