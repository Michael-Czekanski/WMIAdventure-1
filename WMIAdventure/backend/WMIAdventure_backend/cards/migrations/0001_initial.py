# Generated by Django 3.2 on 2021-05-04 15:56

from django.db import migrations, models
from ..models import CardLevel
from ..models import CardEffect


def insert_card_effects_values_to_db(apps, schema_editor):
    CardEffect.objects.all().delete()
    for value in CardEffect.EffectId.values:
        item = CardEffect.objects.create(id=value)
        item.save()


def insert_card_levels_values_to_db(apps, schema_editor):
    """
    Inserts all possible CardLevel records to database.
    """

    CardLevel.objects.all().delete()
    for value in CardLevel.Level.values:
        cLvl = CardLevel.objects.create(level=value)
        cLvl.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CardEffect',
            fields=[
                ('id', models.IntegerField(choices=[(1, 'Zadawanie obrażeń'), (2, 'Tarcza'), (3, 'Losowa zamiana kolejności kart'), (4, 'Zatrzymanie na jedną turę'), (5, 'Dwukrotne wykonanie się karty'), (6, 'Leczenie'), (7, 'Blokowanie następnej karty'), (8, 'Zwiększenie mocy następnej karty'), (9, 'Pomijanie następnej karty')], default=1, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('tooltip', models.TextField(max_length=150, null=True))
                ],
        ),
        migrations.CreateModel(
            name='CardLevel',
            fields=[
                ('level', models.IntegerField(choices=[(1, 'Typowa'), (2, 'Rzadka'), (3, 'Epicka')], default=1, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.RunPython(insert_card_levels_values_to_db),
        migrations.RunPython(insert_card_effects_values_to_db)
    ]