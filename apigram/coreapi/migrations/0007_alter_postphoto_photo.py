# Generated by Django 4.1.5 on 2023-01-06 00:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coreapi', '0006_alter_postphoto_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postphoto',
            name='photo',
            field=models.ImageField(unique=True, upload_to='post_photos', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg'])]),
        ),
    ]
