# Generated by Django 4.1.5 on 2023-01-18 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ledger",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        db_index=True,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                ("memo", models.TextField(default=None, null=True, verbose_name="메모")),
                ("amount", models.BigIntegerField(default=0, verbose_name="예산")),
                ("isActive", models.BooleanField(verbose_name="활성화 여부")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ledger",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="유저",
                    ),
                ),
            ],
            options={
                "verbose_name": "회계",
            },
        ),
    ]