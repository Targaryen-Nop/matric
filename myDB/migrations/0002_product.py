# Generated by Django 4.1.7 on 2023-02-18 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myDB', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.FloatField()),
                ('stock', models.PositiveIntegerField()),
                ('date_add', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
