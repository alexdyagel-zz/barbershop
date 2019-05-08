# Create your models here.
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User as DjangoUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Category(models.Model):
    name = models.CharField(
        max_length=25,
        help_text=_('Название категории'),
        verbose_name=_('название'))

    class Meta:
        verbose_name = _('категория')
        verbose_name_plural = _('категории')

    def __str__(self):
        return self.name


class Service(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        help_text=_('Категория услуги.'),
        verbose_name=_('категория'))
    name = models.CharField(
        max_length=25,
        help_text=_('Название услуги.'),
        verbose_name=_('название'))
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        help_text=_('Цена услуги.'),
        verbose_name=_('цена'))

    class Meta:
        verbose_name = _('услуга')
        verbose_name_plural = _('услуги')

    def __str__(self):
        return self.name


class Specialist(models.Model):
    name = models.CharField(
        max_length=25,
        help_text=_('Имя специалиста.'),
        verbose_name=_('Имя'))
    position = models.CharField(
        max_length=25,
        help_text=_('Должность специалиста.'),
        verbose_name=_('Должность'))
    image = models.ImageField(
        upload_to='profile_image', blank=True,
        help_text=_('Аватар специлиста.'),
        verbose_name=_('аватар'))

    class Meta:
        verbose_name = _('специалист')
        verbose_name_plural = _('специалисты')

    def __str__(self):
        return f'{self.position} {self.name}'


class Seance(models.Model):
    date = models.DateField(
        help_text=_('Дата сеанса.'),
        verbose_name=_('дата'))
    time = models.TimeField(
        help_text=_('Время сеанса.'),
        verbose_name=_('время'))
    specialist = models.ForeignKey(
        Specialist, on_delete=models.CASCADE,
        help_text=_('Специалист.'),
        verbose_name=_('специалист'))
    reserved = models.BooleanField(
        default=False,
        help_text=_('Занят ли сеанс?'),
        verbose_name=_('Зарезервирован'))

    class Meta:
        verbose_name = _('сеанс')
        verbose_name_plural = _('сеансы')

    def __str__(self):
        return f'{self.date} {self.time} {self.specialist}'


class Order(models.Model):
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE,
        help_text=_('Заказанная услуга'),
        verbose_name=_('Услуга'))
    seance = models.ForeignKey(
        Seance, on_delete=models.CASCADE,
        help_text=_('Дата время и специалист'),
        verbose_name=_('Сеанс'))
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        help_text=_('Пользователь, оформивший заказ'),
        verbose_name=_('Пользователь'))

    class Meta:
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')
