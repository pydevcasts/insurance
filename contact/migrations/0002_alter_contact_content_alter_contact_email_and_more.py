# Generated by Django 4.0.1 on 2022-07-20 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='content',
            field=models.TextField(verbose_name='content'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=128, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='subject',
            field=models.CharField(max_length=128, verbose_name='subject'),
        ),
    ]