# Generated by Django 5.1.6 on 2025-03-26 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_customuser_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='Name',
        ),
    ]
