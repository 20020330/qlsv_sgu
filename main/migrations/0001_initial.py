# Generated by Django 4.2.5 on 2023-09-18 11:23

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModAdmin',
            fields=[
                ('id_user', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('username', models.CharField(default=' ', max_length=30, unique=True)),
                ('full_name', models.CharField(max_length=100)),
                ('describe', ckeditor.fields.RichTextField()),
                ('role', models.CharField(choices=[('Member', 'Member'), ('Core Member', 'Core Member'), ('Mentor', 'Mentor'), ('Alumni', 'Alumni')], default='Member', max_length=255)),
                ('mssv', models.CharField(max_length=20)),
                ('class_school', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('image', models.CharField(max_length=5000)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', main.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id_paper', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.TextField(max_length=10000)),
                ('author', models.TextField(max_length=10000)),
                ('abstract', models.TextField(max_length=10000)),
                ('link_paper', models.CharField(default='None', max_length=10000)),
                ('link_github', models.CharField(default='None', max_length=10000)),
                ('institute', models.CharField(default='None', max_length=255)),
                ('interest', models.BooleanField(default=False)),
                ('year', models.IntegerField()),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='papers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id_event', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('image_avatar', models.ImageField(upload_to='main/static/img')),
                ('name_event', models.CharField(max_length=1000)),
                ('content', ckeditor.fields.RichTextField()),
                ('time', models.DateField()),
                ('form_register', models.CharField(default='None', max_length=100)),
                ('id_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
