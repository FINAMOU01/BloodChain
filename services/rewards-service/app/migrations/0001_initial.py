# Generated migration for Reward and Redemption models

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reward',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor_id', models.CharField(max_length=255)),
                ('points', models.IntegerField(default=0)),
                ('reason', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Redemption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor_id', models.CharField(max_length=255)),
                ('reward', models.CharField(max_length=255)),
                ('redeemed_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-redeemed_at'],
            },
        ),
    ]
