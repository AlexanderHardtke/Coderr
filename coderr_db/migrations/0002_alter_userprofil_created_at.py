# Generated by Django 5.1.7 on 2025-03-15 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofil',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
