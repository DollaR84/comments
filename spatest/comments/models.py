from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


User.add_to_class("email", models.EmailField(null=False, blank=False))


# Create your models here.


class Profile(models.Model):
    class Meta:
        db_table = "profiles"
        verbose_name = "User profile"
        verbose_name_plural = "Users profiles"

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="user")
    home_page = models.URLField(null=True, blank=True, verbose_name="home page")


class FileUpload(models.Model):
    class Meta:
        db_table = "files_uploads"
        verbose_name = "File upload"
        verbose_name_plural = "Files uploads"

    filename = models.FileField(upload_to="static/")
    file_type = models.CharField(max_length=4)
    hash_sum = models.CharField(max_length=64, unique=True)


class Comment(models.Model):
    class Meta:
        db_table = "comments"
        verbose_name = "User comment"
        verbose_name_plural = "Users comments"

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE, verbose_name="user")
    text = models.TextField(null=False, blank=False, verbose_name="text comment")
    files = models.ManyToManyField(
        FileUpload, db_table="comments_files_associations",
        null=True, blank=True, verbose_name="files in comment"
    )
    date_time = models.DateTimeField(auto_now_add=True, verbose_name="date and time")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
