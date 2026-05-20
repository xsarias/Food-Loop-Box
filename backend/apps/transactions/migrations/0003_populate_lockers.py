from django.db import migrations


def create_lockers(apps, schema_editor):
    Locker = apps.get_model('transactions', 'Locker')
    # create 15 lockers if they don't already exist
    existing = set(Locker.objects.values_list('numero', flat=True))
    objs = []
    for i in range(1, 16):
        if i in existing:
            continue
        objs.append(Locker(numero=i, estado='libre'))
    if objs:
        Locker.objects.bulk_create(objs)


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_add_locker_and_reservation_field'),
    ]

    operations = [
        migrations.RunPython(create_lockers),
    ]
