# Generated by Django 4.0.1 on 2022-08-30 14:46

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('title', models.CharField(help_text='متن منحصر به فرد باید باشد', max_length=128, unique_for_month='published_at', verbose_name='متن')),
                ('slug', models.CharField(max_length=128, unique_for_month='published_at', verbose_name='اسلاگ')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=1, verbose_name='وضعیت')),
                ('icon', models.CharField(blank=True, max_length=128, null=True, verbose_name='ایکن')),
                ('banner', models.ImageField(blank=True, upload_to='category/%Y/%m/%d', verbose_name='تصویر')),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='پیام')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندیها',
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('title', models.CharField(help_text='متن منحصر به فرد باید باشد', max_length=128, unique_for_month='published_at', verbose_name='متن')),
                ('slug', models.CharField(max_length=128, unique_for_month='published_at', verbose_name='اسلاگ')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=1, verbose_name='وضعیت')),
                ('banner', models.ImageField(blank=True, upload_to='subcategory/%Y/%m/%d', verbose_name='تصویر')),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='پیام')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subcats', to='category.category')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
