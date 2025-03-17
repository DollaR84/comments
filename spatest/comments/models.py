import os
from typeing import Optional

from django.db import models


# Create your models here.


class User(models.Model):
    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    id: int = models.BigAutoField(primary_key=True)
    username: str = models.CharField(max_length=50, null=False, blank=False)
    email: str = models.EmailField(null=False, blank=False, unique=True)
    home_page: Optional[str] = models.URLField(null=True, blank=True, verbose_name="home page")


class FileUpload(models.Model):
    class Meta:
        db_table = "files_uploads"
        verbose_name = "File upload"
        verbose_name_plural = "Files uploads"

    id = models.BigAutoField(primary_key=True)
    file = models.FileField(upload_to="/comments/static/uploads/")


class File(models.Model):
    class Meta:
        db_table = "files"
        verbose_name = "File"
        verbose_name_plural = "Files"

    id: int = models.BigAutoField(primary_key=True)
    file_path: str = models.CharField(max_length=256, unique=True)
    hash_sum: str = models.CharField(max_length=64, editable=False, unique=True)

    @property
    def file_name(self) -> str:
        return os.path.basename(self.file_path)


class Comment(models.Model):
    class Meta:
        db_table = "comments"
        verbose_name = "User comment"
        verbose_name_plural = "Users comments"

    id = models.BigAutoField(primary_key=True)
    parent_id = models.ForeignKey(
        "Comment", on_delete=models.CASCADE,
        related_name="parent_comment", related_query_name="parent_comment",
        null=True, blank=True
    )

    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name="user")
    text = models.TextField(null=False, blank=False, verbose_name="text comment")
    files = models.ManyToManyField(
        File, db_table="comments_files_associations",
        null=True, blank=True, verbose_name="files in comment"
    )
    date_time = models.DateTimeField(auto_now_add=True, verbose_name="date and time")
