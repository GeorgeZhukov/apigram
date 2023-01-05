from django.contrib import admin

from rest_framework.authtoken.admin import TokenAdmin

from .models import Post, PostPhoto, Account

# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(PostPhoto)
class PostPhotoAdmin(admin.ModelAdmin):
    pass



TokenAdmin.raw_id_fields = ['user']
# @admin.register(Post)
# class PostAdmin(admin.ModelAdmin):
#     pass

