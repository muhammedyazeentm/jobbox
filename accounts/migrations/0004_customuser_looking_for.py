# Generated by Django 5.1.6 on 2025-03-06 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_customuser_category_customuser_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='looking_for',
            field=models.CharField(blank=True, choices=[('driver', 'Driver'), ('maid', 'Maid'), ('babysitter', 'Babysitter'), ('gardener', 'Gardener'), ('security_guard', 'Security Guard'), ('other', 'Other')], max_length=50, null=True),
        ),
    ]
