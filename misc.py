import datetime
from calendar import monthrange


def month_end(date: datetime.date):
    assert isinstance(date, datetime.date)
    x, y = monthrange(date.year, date.month)
    return datetime.date(date.year, date.month, y)


def next_month(date: datetime.date):
    assert isinstance(date, datetime.date)
    next_day = date + datetime.timedelta(days=1)
    return month_end(next_day)
