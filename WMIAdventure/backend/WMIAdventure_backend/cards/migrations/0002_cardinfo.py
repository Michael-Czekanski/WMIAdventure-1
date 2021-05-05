# Generated by Django 3.2 on 2021-05-05 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tooltip', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='cards/images/')),
            ],
        ),
    ]
