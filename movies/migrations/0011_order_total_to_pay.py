# Generated by Django 4.1.4 on 2022-12-31 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_to_pay',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]