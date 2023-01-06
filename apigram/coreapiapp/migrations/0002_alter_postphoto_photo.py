# Generated by Django 4.1.5 on 2023-01-06 15:07

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('coreapiapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postphoto',
            name='photo',
            field=imagekit.models.fields.ProcessedImageField(unique=True, upload_to='post_photos'),
        ),
    ]