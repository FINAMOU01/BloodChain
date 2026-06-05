from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor_email', models.EmailField(max_length=254)),
                ('hospital_name', models.CharField(max_length=200)),
                ('appointment_type', models.CharField(default='regular', max_length=100)),
                ('appointment_date', models.DateField()),
                ('appointment_time', models.TimeField()),
                ('status', models.CharField(choices=[('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='confirmed', max_length=20)),
                ('contact_person', models.CharField(blank=True, default='', max_length=200)),
                ('contact_phone', models.CharField(blank=True, default='', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-appointment_date', '-appointment_time'],
            },
        ),
    ]
