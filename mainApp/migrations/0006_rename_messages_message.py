# Generated by Django 4.0 on 2022-01-01 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0005_messages'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Messages',
            new_name='Message',
        ),
    ]
