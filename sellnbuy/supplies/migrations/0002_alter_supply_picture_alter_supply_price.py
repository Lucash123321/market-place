# Generated by Django 4.2.2 on 2023-06-29 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supply',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to='supply/'),
        ),
        migrations.AlterField(
            model_name='supply',
            name='price',
            field=models.CharField(max_length=20),
        ),
    ]
