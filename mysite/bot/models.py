from django.db import models

# Create your models here.

class Video(models.Model):
    name = models.TextField(verbose_name='Название видео')
    discription = models.TextField(verbose_name='Описание видео')
    url_video = models.TextField(verbose_name='Ссылка на полное видео')
    video = models.FileField(verbose_name='Видео')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Видео'


class Profile(models.Model):
    external_id = models.PositiveIntegerField(verbose_name='ID пользователя в телеграмме', unique=True)
    name = models.TextField(verbose_name='Имя пользователя')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    text = models.TextField(verbose_name='Текст для рассылки')
    photo = models.ImageField(verbose_name='Фотография для рассылки', upload_to='images/')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'