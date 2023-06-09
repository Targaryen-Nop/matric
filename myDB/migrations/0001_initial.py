# Generated by Django 4.1.7 on 2023-02-18 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('gender', models.CharField(choices=[('ชาย', 'ชาย'), ('หญิง', 'หญิง')], default='ชาย', max_length=6)),
                ('position', models.CharField(max_length=50)),
                ('salary', models.PositiveIntegerField()),
                ('address', models.TextField()),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('phone', models.CharField(max_length=30, unique=True)),
                ('birthday', models.DateField()),
                ('religion', models.CharField(choices=[('พุทธ', 'พุทธ'), ('คริสต์', 'คริสต์'), ('อิสลาม', 'อิสลาม'), ('อื่นๆ', 'อื่นๆ')], default='พุทธ', max_length=20)),
                ('addition_note', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]
