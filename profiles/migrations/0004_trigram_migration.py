from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('profiles', '0003_profile_address'),
    ]

    operations = [
        TrigramExtension(),
    ]
