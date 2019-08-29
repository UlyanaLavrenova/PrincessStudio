from django.db import models
from django.contrib.auth.models import User
# тип "временнАя зона" для получения текущего времени
from django.utils import timezone


class Master(models.Model):
    fio = models.CharField(max_length=255)
    category = models.CharField(max_length=255)


class Procedure(models.Model):
    procedure_name = models.CharField(max_length=255)
    price = models.IntegerField('price')
    master = models.ForeignKey(Master, on_delete=models.CASCADE, default=0)


class VacantTimes(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, default=0)
    vacant_date_time = models.DateTimeField('datetime')


class Record(models.Model):
    procedure = models.ForeignKey(Procedure, on_delete=models.CASCADE, default=0)
    vacant_time = models.DateTimeField('datetime')
    user = models.ForeignKey(User)


class Message(models.Model):
    chat = models.ForeignKey(Procedure, verbose_name='Отзывы под процедурой', on_delete=models.CASCADE)
    author = models.ForeignKey(User, verbose_name='Пользователь')
    message = models.TextField('Отзыв')
    pub_date = models.DateTimeField('Дата отзыва', default=timezone.now)
