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
    icon_url = models.FileField('Иконка валюты', upload_to='icons/',blank=True, null=True)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
        ordering = ['code_name']

    def __str__(self):
        return self.code_name


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
    period_for_update = models.IntegerField('Частота обновлений в секундах',
                                            blank=True,
                                            null=True,
                                            default=60,
                                            help_text='Значение - положительное целое число.При установлении в 0, останавливает задачу переодических обновлений',
                                            validators=[is_positive_validate])
    # direction_black_list = models.ManyToManyField('Direction', verbose_name='Чёрный список')

    class Meta:
        abstract = True
        verbose_name = 'Обменник'
        verbose_name_plural = 'Обменники'
        ordering = ['name']

    def __str__(self):
        return self.name
    

class BaseDirection(models.Model):
    # valute_from = models.ForeignKey(Valute,
    #                                 to_field='code_name',
    #                                 on_delete=models.CASCADE,
    #                                 verbose_name='Отдаём',
    #                                 limit_choices_to=~Q(type_valute='Наличные'),
    #                                 related_name='no_cash_valutes_from')
    # valute_to = models.ForeignKey(Valute,
    #                               to_field='code_name',
    #                               on_delete=models.CASCADE,
    #                               verbose_name='Получаем',
    #                               limit_choices_to=~Q(type_valute='Наличные'),
    #                               related_name='no_cash_valutes_to')
    
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

    class Meta:
        abstract = True
    #     # unique_together = (("exchange", "valute_from", "valute_to"), )
    #     verbose_name = 'Готовое направление'
    #     verbose_name_plural = 'Готовые направления'
    #     ordering = ['exchange', 'valute_from', 'valute_to']

    # def __str__(self):
    #     return f'{self.exchange} ({self.valute_from} -> {self.valute_to})'