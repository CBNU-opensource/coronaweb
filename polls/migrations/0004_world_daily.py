# Generated by Django 3.0.7 on 2020-06-17 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='World_daily',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('world_date', models.CharField(max_length=200)),
                ('world_confirmed', models.CharField(max_length=200)),
                ('world_confirmed_change', models.CharField(max_length=200)),
                ('world_death', models.CharField(max_length=200)),
                ('world_death_change', models.CharField(max_length=200)),
                ('world_country', models.CharField(max_length=200)),
            ],
        ),
    ]
