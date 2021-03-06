import json

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import authentication
from rest_framework.authtoken.models import Token


class BearerAuthentication(authentication.TokenAuthentication):
    keyword = 'Bearer'


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an user name')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.CharField('biography', max_length=50, blank=True)
    full_name = models.CharField(max_length=50, blank=True)
    profile_photo = models.CharField(max_length=50,blank=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="user_follower")
    followee = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="user_followee")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'followee'], name='follow relation constraint')
        ]

    def __str__(self):
        return str(self.follower) + " follows " + str(self.followee)


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="owner")
    created_at = models.DateTimeField(auto_now_add=True)
    image_link = models.CharField(max_length=200)

    class Meta:
        indexes = [
            models.Index(fields=['owner', 'created_at'])
        ]

    def __str__(self):
        post = {
            'owner': str(self.owner),
            'created_at': str(self.created_at),
            'image': self.image_link
        }
        return json.dumps(post)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
