# Generated by Django 4.2.1 on 2023-06-08 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_user_is_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_changed_password',
            field=models.BooleanField(default=False),
        ),
    ]
