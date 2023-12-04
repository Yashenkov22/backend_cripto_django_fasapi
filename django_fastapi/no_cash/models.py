from django.db import models

from django.db.models import Q

from general_models.models import Valute, BaseExchange, BaseDirection, BaseExchangeDirection


class Exchange(BaseExchange):
    direction_black_list = models.ManyToManyField('Direction', verbose_name='Чёрный список')


class Rating(models.Model):
    # exchange_name = models.CharField(max_length=50, primary_key=True)
    rating = models.CharField(max_length=50, null=True, default=None)
    exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)


class Direction(BaseDirection):
    valute_from = models.ForeignKey(Valute,
                                    to_field='code_name',
                                    on_delete=models.CASCADE,
                                    verbose_name='Отдаём',
                                    limit_choices_to=~Q(type_valute='Наличные'),
                                    related_name='no_cash_valutes_from')
    valute_to = models.ForeignKey(Valute,
                                  to_field='code_name',
                                  on_delete=models.CASCADE,
                                  verbose_name='Получаем',
                                  limit_choices_to=~Q(type_valute='Наличные'),
                                  related_name='no_cash_valutes_to')


class ExchangeDirection(BaseExchangeDirection):
    exchange = models.ForeignKey(Exchange,
                                 on_delete=models.CASCADE,
                                 verbose_name='Обменник',
                                 related_name='directions')
    
    class Meta:
        unique_together = (("exchange", "valute_from", "valute_to"), )
        verbose_name = 'Готовое направление'
        verbose_name_plural = 'Готовые направления'
        ordering = ['exchange', 'valute_from', 'valute_to']

    def __str__(self):
        return f'{self.exchange}:  {self.valute_from} -> {self.valute_to}'