# Generated by Django 4.0.1 on 2022-08-30 14:45

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tag', '__first__'),
        ('category', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='تاریخ ویرایش')),
                ('published_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاریخ انتشار')),
                ('title', models.CharField(help_text='متن منحصر به فرد باید باشد', max_length=128, unique_for_month='published_at', verbose_name='متن')),
                ('slug', models.CharField(max_length=128, unique_for_month='published_at', verbose_name='اسلاگ')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Draft'), (1, 'Published')], default=1, verbose_name='وضعیت')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('summary', models.CharField(max_length=128)),
                ('banner', models.ImageField(blank=True, null=True, upload_to='blog/%Y/%m/%d')),
                ('content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('subcategory', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subcategory', to='category.subcategory')),
                ('tags', models.ManyToManyField(blank=True, related_name='tags', to='tag.Tag')),
            ],
            options={
                'verbose_name': 'پست',
                'verbose_name_plural': 'پستها',
                'ordering': ['-published_at', 'title'],
                'get_latest_by': ['-published_at'],
            },
        ),
    ]
