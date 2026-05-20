# Generated manual migration to add Locker model and add locker FK to Reservation
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Locker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.PositiveIntegerField(unique=True)),
                ('estado', models.CharField(choices=[('libre', 'Libre'), ('ocupado', 'Ocupado')], default='libre', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['numero'],
                'verbose_name': 'Locker',
                'verbose_name_plural': 'Lockers',
            },
        ),
        migrations.AddField(
            model_name='reservation',
            name='locker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reservations', to='transactions.locker'),
        ),
        migrations.AddIndex(
            model_name='locker',
            index=models.Index(fields=['numero'], name='transactions_locker_numero_idx'),
        ),
    ]
