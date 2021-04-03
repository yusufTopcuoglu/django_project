# Generated by Django 3.1.7 on 2021-04-03 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scorp_app', '0009_auto_20210403_1200'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='post',
            name='scorp_app_p_owner_i_f22a4c_idx',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='created',
            new_name='created_at',
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['owner', 'created_at'], name='scorp_app_p_owner_i_af54d1_idx'),
        ),
    ]