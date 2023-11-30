from typing import List

from django.conf import settings

from no_cash.models import NoCashValute


def try_generate_icon_url(valute: NoCashValute) -> str | None:
    icon_url = None
    if valute.icon_url.name:
        icon_url = settings.SITE_DOMAIN\
                    + settings.DJANGO_PREFIX\
                        + valute.icon_url.url
    return icon_url