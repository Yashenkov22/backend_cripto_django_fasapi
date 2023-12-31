from django.db import models

from .utils.model_validators import is_positive_validate


class Valute(models.Model):
    type_valute_list = [
        ('Криптовалюта', 'Криптовалюта'),
        ('Электронные деньги', 'Электронные деньги'),
        ('Балансы криптобирж', 'Балансы криптобирж'),
        ('Интернет-банкинг', 'Интернет-банкинг'),
        ('Денежные переводы', 'Денежные переводы'),
        #
        ('Наличные', 'Наличные'),
        ]
    name = models.CharField('Название валюты',
                            max_length=50,
                            primary_key=True)
    code_name = models.CharField('Кодовое сокращение',
                                 max_length=10,
                                 unique=True)
    type_valute = models.CharField('Тип валюты',
                                   max_length=30,
                                   choices=type_valute_list)
    icon_url = models.FileField('Иконка валюты',
                                upload_to='icons/',
                                blank=True,
                                null=True)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        ordering = ['code_name']

    def __str__(self):
        return self.code_name


class BaseReview(models.Model):
    status_list = [
    ('Опубликован', 'Опубликован'),
    ('Модерация', 'Модерация'),
    ('Отклонён', 'Отклонён'),
    ]
    username = models.CharField('Имя пользователя',
                                max_length=255)
    text = models.TextField('Текст сообщения')
    time_create = models.DateTimeField('Дата создания',
                                       default=None,
                                       blank=True,
                                       null=True,
                                       help_text='Если оставить поля пустыми, время установится автоматически по московскому часовому поясу')
    status = models.CharField('Статус модерации',
                                  max_length=20,
                                  choices=status_list,
                                  default='Модерация',
                                  help_text='При выборе статуса "Отклонён" попадает в очередь на удаление')
    moderation = models.BooleanField('Прошел модерацию?', default=False)

    class Meta:
        abstract = True

    def str_review(self):
        date = self.time_create.strftime("%d.%m.%Y, %H:%M:%S")
        return f' отзыв {self.pk}, Обменник: {self.exchange}, Пользователь: {self.username}, Время создания: {date}'

    def str_comment(self):
        date = self.time_create.strftime("%d.%m.%Y, %H:%M:%S")
        return f' комментарий {self.pk}, Отзыв №{self.review.pk}, Обменник: {self.review.exchange}, Пользователь: {self.username}, Время создания: {date}'


class BaseExchange(models.Model):
    name = models.CharField('Название обменника',
                            max_length=20,
                            primary_key=True)
    xml_url = models.CharField('Ссылка на XML файл',
                               max_length=50)
    partner_link = models.CharField('Партнёрская ссылка',
                                    max_length=50,
                                    blank=True,
                                    null=True,
                                    default=None)
    is_active = models.BooleanField('Статус обменника', default=True)
    period_for_create = models.IntegerField('Частота добавления в секундах',
                                            blank=True,
                                            null=True,
                                            default=90,
                                            help_text='Значение - положительное целое число.При установлении в 0, останавливает задачу переодических добавлений',
                                            validators=[is_positive_validate])
    period_for_update = models.IntegerField('Частота обновлений в секундах',
                                            blank=True,
                                            null=True,
                                            default=60,
                                            help_text='Значение - положительное целое число.При установлении в 0, останавливает задачу переодических обновлений',
                                            validators=[is_positive_validate])
    period_for_parse_black_list = models.IntegerField('Частота парсинга чёрного списка в часах',
                                                      blank=True,
                                                      null=True,
                                                      default=24,
                                                      help_text='Рекомендуемое значение - 24 часа.\nЗначение - положительное целое число.При установлении в 0, останавливает задачу переодического парсинга чёрного списка',
                                                      validators=[is_positive_validate])

    class Meta:
        abstract = True
        verbose_name = 'Обменник'
        verbose_name_plural = 'Обменники'
        ordering = ['name']

    def __str__(self):
        return self.name
    

class BaseDirection(models.Model):
    
    class Meta:
        abstract = True
        unique_together = (("valute_from", "valute_to"), )
        verbose_name = 'Направление для обмена'
        verbose_name_plural = 'Направления для обмена'
        ordering = ['valute_from', 'valute_to']
    
    def __str__(self):
        return self.valute_from.code_name + ' -> ' + self.valute_to.code_name
    

class BaseExchangeDirection(models.Model):
    valute_from = models.CharField('Отдаём', max_length=10)
    valute_to = models.CharField('Получаем', max_length=10)
    in_count = models.FloatField('Сколько отдаём')
    out_count = models.FloatField('Сколько получаем')
    min_amount = models.CharField('Минимальное количество', max_length=50)
    max_amount = models.CharField('Максимальное количество', max_length=50)
    is_active = models.BooleanField('Активно?', default=True)

    class Meta:
        abstract = True