# Generated by Django 4.1.7 on 2023-03-26 22:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_wish_list'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='wish_list',
        ),
    ]
