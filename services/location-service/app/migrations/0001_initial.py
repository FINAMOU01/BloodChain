# Generated migration for Location model with GeoDjango support

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField()),
                ('location_type', models.CharField(choices=[('blood_bank', 'Blood Bank'), ('hospital', 'Hospital')], max_length=20)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
