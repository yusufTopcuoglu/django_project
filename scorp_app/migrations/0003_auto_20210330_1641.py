# Generated by Django 3.1.7 on 2021-03-30 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorp_app', '0002_auto_20210329_2051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='e_mail',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='user_name',
            new_name='username',
        ),
    ]
