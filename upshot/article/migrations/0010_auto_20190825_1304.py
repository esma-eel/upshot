# Generated by Django 2.2.3 on 2019-08-25 08:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0009_auto_20190814_1231'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('-created',)},
        ),
        migrations.AddField(
            model_name='article',
            name='users_negative_vote',
            field=models.ManyToManyField(blank=True, related_name='articles_voted_negative', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='article',
            name='users_positive_vote',
            field=models.ManyToManyField(blank=True, related_name='articles_voted_positive', to=settings.AUTH_USER_MODEL),
        ),
    ]