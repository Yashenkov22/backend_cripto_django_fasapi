from no_cash.models import NoCashValute
from django.conf import settings


def try_get_icon_url(valute: NoCashValute) -> str | None:
    icon = None
    if valute.icon_url.name:
        icon = valute.icon_url.url

    return None if not icon else settings.SITE_DOMAIN + '/django' + icon