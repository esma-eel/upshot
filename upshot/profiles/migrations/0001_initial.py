# Generated by Django 4.2.6 on 2023-10-15 12:11

import upshot.profiles.utils.upload_path
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_removed", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        unique=True,
                        verbose_name="UUID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True,
                        max_length=32,
                        null=True,
                        verbose_name="Name",
                    ),
                ),
                (
                    "avatar",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to=upshot.profiles.utils.upload_path.profile_upload,
                        verbose_name="Avatar",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProfilePhoneNumber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_removed", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "number",
                    models.CharField(
                        max_length=11, unique=True, verbose_name="Number"
                    ),
                ),
                ("is_primary", models.BooleanField(default=False)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="phone_number_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProfileEmail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_removed", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "email",
                    models.EmailField(
                        max_length=254, unique=True, verbose_name="Email"
                    ),
                ),
                ("is_primary", models.BooleanField(default=False)),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="email_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ProfileAddress",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_removed", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "city",
                    models.CharField(
                        blank=True,
                        max_length=32,
                        null=True,
                        verbose_name="City",
                    ),
                ),
                ("address", models.TextField(verbose_name="Address")),
                (
                    "profile",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="address_set",
                        to="profiles.profile",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
