from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=50)
    e_mail = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    bio = models.CharField('biography', max_length=50)
    full_name = models.CharField(max_length=50)
    profile_photo = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name


