# Generated by Django 4.1.5 on 2023-01-19 05:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ledger", "0004_alter_ledger_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="ledger",
            options={"ordering": ["-created_at"], "verbose_name": "가계부"},
        ),
    ]