# Generated by Django 5.1 on 2024-09-25 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0003_subscription"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True, verbose_name="ОДата последнего изменения урока"
            ),
        ),
    ]
