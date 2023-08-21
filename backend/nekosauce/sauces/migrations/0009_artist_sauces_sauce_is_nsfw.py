# Generated by Django 4.2.4 on 2023-08-17 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sauces', '0008_artist_sauce_type_alter_sauce_downloaded_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='artist',
            name='sauces',
            field=models.ManyToManyField(blank=True, related_name='artists', to='sauces.sauce'),
        ),
        migrations.AddField(
            model_name='sauce',
            name='is_nsfw',
            field=models.BooleanField(default=False),
        ),
    ]