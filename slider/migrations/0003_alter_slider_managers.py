# Generated by Django 4.0.1 on 2022-09-13 09:28

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('slider', '0002_remove_slider_banner'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='slider',
            managers=[
                ('condition', django.db.models.manager.Manager()),
            ],
        ),
    ]