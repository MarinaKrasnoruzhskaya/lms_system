from datetime import datetime, timedelta

import pytz

from config import settings


def is_difference_datetime(datetime_, hours=0, days=0):
    """Функция сравнивает разницу между текущим временем и переданным datetime и интервалом времени в часах и днях """

    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    print(current_datetime - datetime_)
    print(timedelta(days=days, hours=hours))
    print(current_datetime - datetime_ >= timedelta(days=days, hours=hours))
    return current_datetime - datetime_ >= timedelta(days=days, hours=hours)
