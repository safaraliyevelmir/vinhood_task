# Generated by Django 4.1.7 on 2023-03-29 21:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_rename_product_category_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]