# Generated by Django 2.2.5 on 2019-09-20 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0005_auto_20190919_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='class_name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='class_name_fa',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='score',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='xmax',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='xmin',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='ymax',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='category',
            name='ymin',
            field=models.FloatField(),
        ),
    ]
