from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Users require an email field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    cloud_profile_image = CloudinaryField('image', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class NewPost(models.Model):
    title = models.CharField(max_length=64, blank=False, null=False)
    body = models.TextField(max_length=640, null=False, blank=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_post')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"


class Bookmark(models.Model):
    post = models.ForeignKey(NewPost, on_delete=models.CASCADE, related_name='post_bookmark')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bookmark')
    created_at = models.DateTimeField(auto_now_add=True)
    bookmarked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.post}"