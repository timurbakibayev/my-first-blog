# Generated by Django 4.0.3 on 2022-05-05 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_cart_item_cartitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-id']},
        ),
    ]
