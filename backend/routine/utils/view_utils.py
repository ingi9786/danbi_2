from ..models import RoutineResult



def logical_delete_routine_result(instance):
    result = RoutineResult.objects.get(routine=instance.id)
    result.is_deleted = True
    result.save()

def logical_delete_routine(instance):
    instance.is_deleted = True
    instance.save()
    logical_delete_routine_result(instance)

def get_LIST_response_msg(request):
    date    = bool(request.GET.get('date', None))
    deleted = bool(request.GET.get('is-del', None))

    prefix = ''
    if date==False and deleted==False:
        prefix = ''
    elif date==True:
        prefix = 'DATED '
    elif deleted==True:
        prefix = 'DELETED '

    msg = f"You have successfully lookup the {prefix}routine list."
    return msg