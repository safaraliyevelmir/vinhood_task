# Generated by Django 4.1.7 on 2023-03-26 23:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_wishlistitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='product_category',
            new_name='category',
        ),
    ]
