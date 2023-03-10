# Generated by Django 4.1.4 on 2022-12-31 09:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0009_rename_day_time_time_time_day_movie_seat_day_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=200, null=True)),
                ('movie_title', models.CharField(max_length=255)),
                ('seat_number', models.CharField(max_length=200)),
                ('order_status', models.CharField(choices=[(1, 'cancle'), (2, 'paid'), (3, 'in progress')], max_length=200)),
                ('show_day', models.CharField(max_length=200)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
