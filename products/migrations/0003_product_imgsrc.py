# Generated by Django 4.1 on 2023-04-15 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_category_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imgsrc',
            field=models.CharField(default='', max_length=255),
        ),
    ]
