# Generated by Django 5.1.3 on 2024-11-11 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='binancedata',
            name='price',
            field=models.DecimalField(decimal_places=4, max_digits=20),
        ),
        migrations.AlterField(
            model_name='binancedata',
            name='symbol',
            field=models.CharField(max_length=10),
        ),
    ]