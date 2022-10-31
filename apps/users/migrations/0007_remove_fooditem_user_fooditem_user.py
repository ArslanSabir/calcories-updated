# Generated by Django 4.0.4 on 2022-06-02 18:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_fooditem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fooditem',
            name='user',
        ),
        migrations.AddField(
            model_name='fooditem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='foods', to=settings.AUTH_USER_MODEL),
        ),
    ]