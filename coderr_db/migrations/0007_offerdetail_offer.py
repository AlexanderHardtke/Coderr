# Generated by Django 5.1.7 on 2025-03-24 09:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coderr_db', '0006_remove_offerdetail_offer_alter_offerdetail_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerdetail',
            name='offer',
            field=models.OneToOneField(default="", on_delete=django.db.models.deletion.CASCADE, related_name='details', to='coderr_db.offer'),
        ),
    ]
