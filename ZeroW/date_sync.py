from datetime import datetime, timezone, timedelta

def update_date():
    timezone_offset = 0
    tzinfo = timezone(timedelta(hours=timezone_offset))
    datestr = datetime.now(tzinfo).strftime('%a, %d.%m.%Y %H:%M')
    return datestr