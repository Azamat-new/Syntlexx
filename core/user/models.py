from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail



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



