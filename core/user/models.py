from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.http import HttpResponse

from tour.models import Tour, Booking
import csv


class MyUserManager(BaseUserManager):
    def create_user(self, phone_number, username, password=None):
        if not phone_number:
            raise ValueError('Пользователи должны иметь номер телефона')

        user = self.model(
            phone_number=phone_number,
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, username, password=None):
        user = self.create_user(
            phone_number=phone_number,
            username=username
        )
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField('Имя', max_length=123)
    phone_number = models.CharField('Номер телефона', max_length=17, unique=True)
    email = models.EmailField('Электронная почта', blank=True, null=True)
    created_date = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_date = models.DateTimeField('Дата обновления', auto_now=True)
    avatar = models.ImageField('Аватарка', upload_to='avatars/', blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Обычный пользователь'),
            (2, 'Менеджер'),
            (3, 'Консультант'),
            (4, 'Администратор'),
            (5, 'Автор туру'),
        ),
        default=1,
        verbose_name='Роль пользователя'
    )
    is_admin = models.BooleanField('Является администратором', default=False)
    is_superuser = models.BooleanField(default=False)

    favorite_tours = models.ManyToManyField('tour.Tour', related_name='favorited_by_users', blank=True)
    bookings = models.ManyToManyField('tour.Booking', blank=True, related_name='users')

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone_number', 'email', 'status', 'is_admin')
    search_fields = ('username', 'phone_number', 'email')
    list_filter = ('status', 'is_admin')

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'available_seats')
    search_fields = ('title', 'category')
    list_filter = ('category', 'price')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('tour', 'user', 'date', 'status', 'total_price')
    search_fields = ('tour__title', 'user__username')
    list_filter = ('status', 'date')

@admin.action(description='Выгрузить отчеты по бронированиям')
def export_bookings_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="bookings.csv"'
    writer = csv.writer(response)
    writer.writerow(['Tour', 'User', 'Date', 'Status', 'Total Price'])

    for booking in queryset:
        writer.writerow([booking.tour, booking.user, booking.date, booking.status, booking.total_price])

    return response

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    actions = [export_bookings_to_csv]

@receiver(post_save, sender=Tour)
def send_tour_creation_notification(sender, instance, created, **kwargs):
    if created:
        send_mail(
            'Новый тур создан',
            f'Тур "{instance.title}" был успешно создан!',
            'admin@yourapp.com',
            [instance.author.email],
        )

