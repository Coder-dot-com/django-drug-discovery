# Generated by Django 5.0.7 on 2024-07-10 11:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('generate_molecules', '0013_target_chembl_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='generationrequest',
            name='organism',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='generate_molecules.organism'),
        ),
    ]
