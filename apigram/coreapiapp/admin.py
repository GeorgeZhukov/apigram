from django.contrib import admin

from rest_framework.authtoken.admin import TokenAdmin

from .models import Post, PostPhoto, Account

# Register your models here.




@admin.register(PostPhoto)
class PostPhotoAdmin(admin.ModelAdmin):
    pass

class PostPhotosInlineAdmin(admin.StackedInline):
    model = PostPhoto
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostPhotosInlineAdmin]

TokenAdmin.raw_id_fields = ['user']


