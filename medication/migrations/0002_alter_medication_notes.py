# Generated by Django 3.2.7 on 2021-10-01 02:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("medication", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="medication",
            name="notes",
            field=models.TextField(blank=True),
        ),
    ]
