# Generated by Django 2.2.5 on 2019-09-20 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0008_category_class_name_fa'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='area',
            field=models.FloatField(default=0),
        ),
    ]
