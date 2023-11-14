from django.db import models


class Exchange(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    xml_url = models.CharField(max_length=50)
    partner_link = models.CharField(max_length=50, blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Обменник'
        verbose_name_plural = 'Обменники'

    def __str__(self):
        return self.name


class Rating(models.Model):
    exchange_name = models.CharField(max_length=50, primary_key=True)
    rating = models.CharField(max_length=50, null=True, default=None)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)


class NoCashValute(models.Model):
    type_list = [
        ('Криптовалюта', 'Криптовалюта'),
        ('Электронные деньги', 'Электронные деньги'),
        ('Балансы криптобирж', 'Балансы криптобирж'),
        ('Интернет-банкинг', 'Интернет-банкинг'),
        ('Денежные переводы', 'Денежные переводы'),
        ]
    name = models.CharField(max_length=50, primary_key=True)
    code_name = models.CharField(max_length=10, unique=True)
    type_valute = models.CharField(max_length=30, choices=type_list)

    class Meta:
        verbose_name = 'Безналичная валюта'
        verbose_name_plural = 'Безналичные валюты'

    def __str__(self):
        return self.code_name


class Direction(models.Model):
    valute_from = models.ForeignKey(NoCashValute,
                                    to_field='code_name',
                                    on_delete=models.CASCADE,
                                    verbose_name='Отдаём',
                                    related_name='valutes_from')
    valute_to = models.ForeignKey(NoCashValute,
                                  to_field='code_name',
                                  on_delete=models.CASCADE,
                                  verbose_name='Получаем',
                                  related_name='valutes_to')
    
    class Meta:
        unique_together = (("valute_from", "valute_to"), )
        verbose_name = 'Направление для обмена'
        verbose_name_plural = 'Направления для обмена'        
    
    def __str__(self):
        return self.valute_from.code_name + ' -> ' + self.valute_to.code_name


class ExchangeDirection(models.Model):
    exchange_name = models.ForeignKey(Exchange,
                                      on_delete=models.CASCADE,
                                      verbose_name='Обменник')
    valute_from = models.CharField('Отдаём', max_length=10)
    valute_to = models.CharField('Получаем', max_length=10)
    in_count = models.FloatField('Сколько отдаём')
    out_count = models.FloatField('Сколько получаем')
    min_amount = models.CharField('Минимальное количество', max_length=50)
    max_amount = models.CharField('Максимальное количество', max_length=50)

    class Meta:
        verbose_name = 'Готовое направление'
        verbose_name_plural = 'Готовые направления'
        ordering = ['exchange_name']

    def __str__(self):
        return f'{self.exchange_name} ({self.valute_from} -> {self.valute_to})'
