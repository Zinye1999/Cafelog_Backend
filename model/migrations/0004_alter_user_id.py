# Generated by Django 5.0 on 2023-12-26 18:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("model", "0003_user_created_at_user_updated_at_alter_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
