# Generated by Django 5.1.6 on 2025-04-08 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travel', '0002_category_route_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]
