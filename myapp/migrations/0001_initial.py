# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Taqiinfo',
            fields=[
                ('cityid', models.IntegerField(serialize=False, primary_key=True, db_column='CityID')),
                ('weatherdate', models.DateField(db_column='WeatherDate')),
                ('updatedt', models.DateTimeField(null=True, db_column='UpdateDT', blank=True)),
                ('aqi', models.IntegerField(null=True, db_column='AQI', blank=True)),
                ('pm10', models.IntegerField(null=True, db_column='PM10', blank=True)),
                ('pm25', models.IntegerField(null=True, db_column='PM25', blank=True)),
                ('no2', models.IntegerField(null=True, db_column='NO2', blank=True)),
                ('so2', models.IntegerField(null=True, db_column='SO2', blank=True)),
                ('co', models.FloatField(null=True, db_column='CO', blank=True)),
                ('o3', models.IntegerField(null=True, db_column='O3', blank=True)),
            ],
            options={
                'db_table': 'TAQIInfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tcitybaseinfo',
            fields=[
                ('cityid', models.IntegerField(serialize=False, primary_key=True, db_column='CityID')),
                ('name', models.CharField(max_length=30, db_column='Name')),
                ('alphacode', models.CharField(max_length=80, null=True, db_column='AlphaCode', blank=True)),
                ('provincecode', models.CharField(max_length=50, null=True, db_column='ProvinceCode', blank=True)),
            ],
            options={
                'db_table': 'TCityBaseInfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tdayweather',
            fields=[
                ('cityid', models.IntegerField(serialize=False, primary_key=True, db_column='CityID')),
                ('weatherdate', models.DateField(db_column='WeatherDate')),
                ('updatedt', models.DateTimeField(null=True, db_column='UpdateDT', blank=True)),
                ('nowtemp', models.IntegerField(null=True, db_column='NowTemp', blank=True)),
                ('maxtemp', models.IntegerField(null=True, db_column='MaxTemp', blank=True)),
                ('mintemp', models.IntegerField(null=True, db_column='MinTemp', blank=True)),
                ('weather', models.CharField(max_length=10, null=True, db_column='Weather', blank=True)),
                ('nowwinddirectionid', models.CharField(max_length=10, null=True, db_column='NowWindDirectionID', blank=True)),
                ('startwinddirectionid', models.CharField(max_length=10, null=True, db_column='StartWindDirectionID', blank=True)),
                ('endwinddirectionid', models.CharField(max_length=10, null=True, db_column='EndWindDirectionID', blank=True)),
                ('windscale', models.CharField(max_length=10, null=True, db_column='WindScale', blank=True)),
                ('humidity', models.FloatField(null=True, db_column='Humidity', blank=True)),
                ('aqi', models.CharField(max_length=20, null=True, db_column='AQI', blank=True)),
            ],
            options={
                'db_table': 'TDayWeather',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tdetailweather',
            fields=[
                ('cityid', models.IntegerField(serialize=False, primary_key=True, db_column='CityID')),
                ('weathertime', models.DateTimeField(db_column='WeatherTime')),
                ('temp', models.IntegerField(null=True, db_column='Temp', blank=True)),
                ('weather', models.CharField(max_length=10, null=True, db_column='Weather', blank=True)),
            ],
            options={
                'db_table': 'TDetailWeather',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tprovincebaseinfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, null=True, db_column='Name', blank=True)),
                ('alphacode', models.CharField(max_length=50, null=True, db_column='AlphaCode', blank=True)),
            ],
            options={
                'db_table': 'TProvinceBaseInfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tupdaterecord',
            fields=[
                ('cityid', models.IntegerField(serialize=False, primary_key=True, db_column='CityID')),
                ('lastupdatedt', models.DateTimeField(null=True, db_column='LastUpdateDT', blank=True)),
            ],
            options={
                'db_table': 'TUpdateRecord',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Twinddirectionbaseinfo',
            fields=[
                ('windid', models.IntegerField(serialize=False, primary_key=True, db_column='WindID')),
                ('name', models.CharField(max_length=10, null=True, db_column='Name', blank=True)),
                ('icon', models.CharField(max_length=100, null=True, db_column='Icon', blank=True)),
            ],
            options={
                'db_table': 'TWindDirectionBaseInfo',
                'managed': False,
            },
        ),
    ]
