# Generated by Django 3.2.8 on 2021-11-16 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='favorites',
            constraint=models.UniqueConstraint(fields=('user', 'product'), name='unique_favorite'),
        ),
    ]
