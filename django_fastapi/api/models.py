from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .services import xml_parser


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



#Signal to add direction for every exchange
@receiver(post_save, sender=Direction)
def add_directions_to_exchanges(sender, instance, created, **kwargs):
    if created:
        exchange_list = Exchange.objects.all()
        for exchange in exchange_list:
            dict_for_parser = exchange.__dict__ | instance.__dict__
            print(dict_for_parser)
            dict_for_exchange_direction = xml_parser(dict_for_parser)
            dict_for_exchange_direction['exchange_name'] = exchange
            ExchangeDirection.objects.create(**dict_for_exchange_direction)
            print('DONE')
            # break
        
        # if list_orders_on_wait:
        #     list_email_for_sending = tuple(map(lambda order: order.customer.email,
        #                                        list_orders_on_wait))
        #     model, version = instance.serial.split('-')
            
        #     #Run celery task
        #     background_send_email.delay(list_email_for_sending,
        #                                 model,
        #                                 version)
            
        #     #Delete orders waiting this robot
        #     list_orders_on_wait.delete()