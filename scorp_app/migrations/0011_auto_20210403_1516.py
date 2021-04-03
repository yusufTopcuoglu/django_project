# Generated by Django 3.1.7 on 2021-04-03 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorp_app', '0010_auto_20210403_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, max_length=50, verbose_name='biography'),
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
