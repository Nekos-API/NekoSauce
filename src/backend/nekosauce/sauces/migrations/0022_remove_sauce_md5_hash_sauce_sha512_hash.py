# Generated by Django 4.2.4 on 2023-09-06 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sauces', '0021_alter_hash_bits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sauce',
            name='md5_hash',
        ),
        migrations.AddField(
            model_name='sauce',
            name='sha512_hash',
            field=models.CharField(db_index=True, max_length=128, null=True),
        ),
    ]
