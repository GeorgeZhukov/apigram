# Generated by Django 4.1.5 on 2023-01-10 00:49

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('coreapiapp', '0004_alter_accountphoto_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountphoto',
            name='photo',
            field=imagekit.models.fields.ProcessedImageField(default='account_photos/default.jpg', upload_to='account_photos'),
        ),
    ]
