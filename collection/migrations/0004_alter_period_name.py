# Generated by Django 4.2.6 on 2023-11-01 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0003_alter_artwork_date_alter_genre_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='period',
            name='name',
            field=models.CharField(max_length=80, unique=True),
        ),
    ]
