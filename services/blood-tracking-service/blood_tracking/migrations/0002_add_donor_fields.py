from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blood_tracking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloodbag',
            name='donor_email',
            field=models.EmailField(blank=True, help_text='Donor who provided this blood', max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='bloodbag',
            name='hospital_name',
            field=models.CharField(blank=True, default='', help_text='Hospital/clinic where collected', max_length=200),
        ),
        migrations.AddField(
            model_name='bloodbag',
            name='volume_ml',
            field=models.PositiveIntegerField(default=450, help_text='Blood volume in milliliters'),
        ),
    ]
