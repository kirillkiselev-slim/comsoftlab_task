from django.db import models
from django.contrib.auth.models import User


class EmailAccount(models.Model):
    user = models.ForeignKey(
        User, related_name='email_accounts', on_delete=models.CASCADE,
        verbose_name='Пользователь')
    email_address = models.EmailField(
        verbose_name='Адрес электронной почты',
        unique=True)
    password = models.CharField(max_length=255, verbose_name='Пароль')
    service_provider = models.CharField(
        max_length=100, verbose_name='Почтовый сервис', choices=[
            ('gmail', 'Gmail'),
            ('yandex', 'Yandex'),
            ('mail_ru', 'Mail.ru'),
        ])

    def __str__(self):
        return self.email_address


class Message(models.Model):
    subject = models.TextField(max_length=1000,
                               verbose_name='Тема сообщения',
                               null=False, blank=False)
    date_sent = models.DateTimeField(
        blank=False, null=False,
        verbose_name='Дата отправки'
    )
    date_received = models.DateTimeField(
        blank=False, null=False,
        verbose_name='Дата получения'
    )
    email_body = models.TextField(max_length=380000,
                                  verbose_name='Текст сообщения',
                                  null=False, blank=False)
    user = models.ForeignKey(User, related_name='messages',
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    email_account = models.ForeignKey(
        EmailAccount, related_name='messages',
        on_delete=models.CASCADE,
        verbose_name='Почтовый аккаунт')

    def __str__(self):
        return self.subject


class Attachment(models.Model):
    message = models.ForeignKey(
        Message, related_name='attachments',
        on_delete=models.CASCADE,
        verbose_name='Сообщение')
    file_name = models.CharField(max_length=255,
                                 verbose_name='Имя файла')
    file = models.FileField(upload_to='attachments/',
                            verbose_name='Файл')
    file_size = models.PositiveIntegerField(verbose_name='Размер файла',
                                            null=True, blank=True)

    def __str__(self):
        return self.file_name
