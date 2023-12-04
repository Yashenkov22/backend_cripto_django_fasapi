from django.core.management.base import BaseCommand, CommandError

from cash.models import Country, City

class Command(BaseCommand):
    print('Creating Cities')

    def handle(self, *args, **kwargs):
        try:
            for city in open('cities.txt'):
                city = tuple(map(lambda el: el.strip(), city.split(',')))
                code_name, name, country_name = city
                country = Country.objects.get(name=country_name)
                City.objects.create(name=name,
                                    code_name=code_name,
                                    country=country)
        except Exception as ex:
            print(ex)
            raise CommandError('Initalization failed.')