from django.contrib import admin

from rest_framework.authtoken.admin import TokenAdmin

from .models import Post, PostPhoto, Account, AccountPhoto

# Register your models here.


@admin.register(PostPhoto)
class PostPhotoAdmin(admin.ModelAdmin):
    autocomplete_fields = ['author', 'post']
    search_fields = ['author__user__username']
    list_filter = ['author__user__username',]


class PostPhotosInlineAdmin(admin.StackedInline):
    model = PostPhoto
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostPhotosInlineAdmin]

    search_fields = ['author__user__username', ]


class AccountPhotoAdmin(admin.StackedInline):
    model = AccountPhoto
    extra = 0


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    search_fields = ['user__username', ]
    readonly_fields = ['user', 'created_at', 'updated_at']
    inlines = [AccountPhotoAdmin]


TokenAdmin.raw_id_fields = ['user']
