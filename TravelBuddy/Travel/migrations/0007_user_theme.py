# Generated by Django 5.2 on 2025-04-13 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travel', '0006_alter_route_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='theme',
            field=models.CharField(default='light', max_length=20),
        ),
    ]
