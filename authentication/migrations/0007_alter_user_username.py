# Generated by Django 4.2.1 on 2023-05-24 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_user_about_user_contact_no_user_firstname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='user', max_length=20, verbose_name='Username'),
        ),
    ]
