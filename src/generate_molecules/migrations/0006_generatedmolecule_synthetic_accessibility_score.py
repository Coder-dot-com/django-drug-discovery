# Generated by Django 5.0.6 on 2024-07-07 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate_molecules', '0005_fromcompounds_fromtarget_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='generatedmolecule',
            name='synthetic_accessibility_score',
            field=models.DecimalField(decimal_places=3, default=1, max_digits=100),
            preserve_default=False,
        ),
    ]
