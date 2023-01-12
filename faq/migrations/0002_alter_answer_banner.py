# Generated by Django 4.0.1 on 2023-01-09 20:04

from django.db import migrations, models
import painless.models.validations


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='answer/%Y/%m/%d', validators=[painless.models.validations.validate_file_extension, painless.models.validations.validate_file_size], verbose_name='آپلود فایل'),
        ),
    ]
