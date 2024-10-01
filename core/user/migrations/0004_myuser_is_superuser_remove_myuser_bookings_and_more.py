# Generated by Django 5.0.6 on 2024-09-24 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0002_alter_booking_user'),
        ('user', '0003_myuser_bookings_myuser_favorite_tours'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
        migrations.RemoveField(
            model_name='myuser',
            name='bookings',
        ),
        migrations.AlterField(
            model_name='myuser',
            name='favorite_tours',
            field=models.ManyToManyField(blank=True, related_name='favorited_by_users', to='tour.tour'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='is_admin',
            field=models.BooleanField(default=False, verbose_name='Является администратором'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Обычный пользователь'), (2, 'Менеджер'), (3, 'Консультант'), (4, 'Администратор')], default=1, verbose_name='Роль пользователя'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='bookings',
            field=models.ManyToManyField(blank=True, related_name='users', to='tour.booking'),
        ),
    ]
