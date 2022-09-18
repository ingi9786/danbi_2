from datetime import date
from ..models import RoutineResult

def logical_delete_routine_result(instance):
    result = RoutineResult.objects.get(routine=instance.id)
    result.is_deleted = True
    result.save()

def logical_delete_routine(instance):
    instance.is_deleted = True
    instance.save()
    logical_delete_routine_result(instance)

def convert_day(arg):
    daydic = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    y = int(arg[:4])
    m = int(arg[4:6])
    d = int(arg[6:])
    _date = date(y, m, d)
    _day  = _date.weekday()
    return daydic[_day]

def get_today():
    return "".join(str(date.today()).split('-'))

def is_valid_date(arg):
    return True if arg.isdigit() and len(arg)==8 else False