# Generated by Django 4.0.4 on 2022-05-29 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_profile_os_profile_complete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='os_profile_complete',
            new_name='is_profile_complete',
        ),
    ]
