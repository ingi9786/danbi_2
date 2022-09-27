from datetime import date


def convert_day(arg):
    daydic = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    y = int(arg[:4])
    m = int(arg[4:6])
    d = int(arg[6:])
    _date = date(y, m, d)
    _day  = date.weekday(_date)
    return daydic[_day]

def is_valid_date(arg):
    return True if arg.isdigit() and len(arg)==8 else False