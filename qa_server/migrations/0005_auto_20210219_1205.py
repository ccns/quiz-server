# Generated by Django 3.1.5 on 2021-02-19 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qa_server", "0004_auto_20210123_1428"),
    ]

    operations = [
        migrations.AlterField(
            model_name="player",
            name="platform",
            field=models.CharField(
                choices=[
                    ("Messenger", "Messenger"),
                    ("Telegram", "Telegram"),
                    ("Discord", "Discord"),
                    ("Netcat", "Netcat"),
                    ("Line", "Line"),
                    ("Mewe", "Mewe"),
                ],
                default="Discord",
                max_length=16,
            ),
        ),
    ]
