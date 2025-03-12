from django.contrib import admin

# Register your models here.

from .models import Comment, FileUpload, User


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "id", "user", "date_time",
    )


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "id", "filename", "file_type", "hash_sum",
    )


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    empty_value_display = "-empty-"
    list_display = (
        "id", "username", "email", "home_page",
    )
