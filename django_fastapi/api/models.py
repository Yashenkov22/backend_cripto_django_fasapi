from django.db import models


class Exchange(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    xml_url = models.CharField(max_length=50)
    partner_link = models.CharField(max_length=50, blank=True, null=True, default=None)


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

    def __str__(self):
        return self.code_name


class Direction(models.Model):
    valute_from = models.ForeignKey(NoCashValute,
                                    to_field='code_name',
                                    on_delete=models.CASCADE,
                                    related_name='valutes_from')
    valute_to = models.ForeignKey(NoCashValute,
                                  to_field='code_name',
                                  on_delete=models.CASCADE,
                                  related_name='valutes_to')
    
    direction_name = models.CharField(max_length=20, unique=True)
    
    class Meta:
        unique_together = (("valute_from", "valute_to"),)
    
    def __str__(self):
        return self.valute_from.code_name + '->' + self.valute_to.code_name


class ExchangeDirection(models.Model):
    exchange_name = models.ForeignKey(Exchange, on_delete=models.CASCADE)
    valute_from = models.CharField(max_length=10)
    valute_to = models.CharField(max_length=10)
    in_count = models.FloatField()
    out_count = models.FloatField()
    min_amount = models.CharField(max_length=50)
    max_amount = models.CharField(max_length=50)
