# Generated by Django 3.1.7 on 2021-04-03 11:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scorp_app', '0007_post'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='post',
            index_together={('owner', 'created')},
        ),
    ]
