# Generated by Django 4.2.20 on 2025-04-05 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voter_analytics", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="voter",
            name="precinct_number",
            field=models.CharField(max_length=10),
        ),
    ]
