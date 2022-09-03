# Generated by Django 4.0.1 on 2022-08-30 14:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatar/%Y/%m/%d', verbose_name='آپلود فایل')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')),
                ('gender', models.PositiveSmallIntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female')], default=1, null=True, verbose_name='جنسیت')),
                ('phone', models.CharField(blank=True, max_length=12, null=True, verbose_name=' تلفن ثابت')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name=' آدرس')),
                ('city', models.CharField(blank=True, max_length=50, null=True, verbose_name='شهر')),
                ('zip', models.CharField(blank=True, max_length=30, null=True, verbose_name='کد پستی')),
                ('instagram', models.URLField(blank=True, null=True, verbose_name='اینستاگرام')),
                ('whatsapp', models.URLField(blank=True, null=True, verbose_name='واتس آپ')),
                ('linkedin', models.URLField(blank=True, null=True, verbose_name='لینکدین')),
                ('about', models.TextField(blank=True, null=True, verbose_name='درباره خود بنویسید')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'پروفایل',
                'verbose_name_plural': 'پروفایل',
            },
        ),
    ]
