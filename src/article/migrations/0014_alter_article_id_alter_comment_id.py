# Generated by Django 4.2 on 2024-02-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_auto_20190827_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]