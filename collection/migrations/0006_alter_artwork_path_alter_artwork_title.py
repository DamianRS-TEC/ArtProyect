# Generated by Django 4.2.6 on 2023-11-01 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_alter_period_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artwork',
            name='path',
            field=models.CharField(max_length=300, unique=True),
        ),
        migrations.AlterField(
            model_name='artwork',
            name='title',
            field=models.CharField(max_length=300),
        ),
    ]
