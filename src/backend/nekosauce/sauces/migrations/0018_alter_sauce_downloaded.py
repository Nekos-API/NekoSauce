# Generated by Django 4.2.4 on 2023-09-05 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sauces', '0017_alter_sauce_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sauce',
            name='downloaded',
            field=models.BooleanField(db_index=True, default=False, null=True),
        ),
    ]
