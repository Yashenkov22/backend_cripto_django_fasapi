import os
# from asgiref.sync import sync_to_async
# import requests

# from bs4 import BeautifulSoup, NavigableString

from django.apps import apps
from django.conf import settings
from django.core.wsgi import get_wsgi_application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
apps.populate(settings.INSTALLED_APPS)


from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from starlette.middleware.cors import CORSMiddleware

# from api.models import Exchange, Rating

from api.endpoints import api_router


def get_application() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix="/api")
    app.mount("/django", WSGIMiddleware(get_wsgi_application()))

    return app


app = get_application()

# WORK!

# def parse_rate():
#     resp = requests.get('https://www.bestchange.ru/list.html')

#     soup = BeautifulSoup(resp.text, 'lxml')
#     rows = soup.find('table', id='content_table').find('tbody').find_all('td', class_='rw')
    
#     if rows: 
#         rating_dict = {}

#         for row in rows:
#             row: NavigableString
#             exchange_name = row.find('a').get('title').split()[-1]
#             rating_table = row.find('table').find('tr').find_all('td')
#             rating = []
#             for rating_part in rating_table:
#                 if rating_part.text.isdigit():
#                     rating.append(rating_part.text)
#             rating_dict[exchange_name] = '/'.join(rating[::-1])

#         return rating_dict
    

# def create_rating():
#     exchange_list = Exchange.objects.all()
#     rating_dict = parse_rate()
#     for exchange in exchange_list:
#         Rating.objects.create(exchange_name=exchange.name,
#                               rating=rating_dict.get(exchange.name),
#                               exchange=exchange)


# create_rating()
    
# print(parse_rate())