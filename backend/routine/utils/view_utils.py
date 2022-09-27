from ..models import Routine, RoutineResult



def logical_delete_routine(routine):
    routine.soft_delete()
    result = RoutineResult.objects.get(routine=routine)
    result.soft_delete()

def get_LIST_response_msg(request):
    date    = bool(request.GET.get('date', None))
    deleted = request.GET.get('is-del', None)
    if deleted == None or '0':
        deleted = False
    else:
        deleted = True

    prefix = ''
    if date==False and deleted==False:
        prefix = ''
    elif date==True:
        prefix = 'DATED '
    elif deleted==True:
        prefix = 'DELETED '

    msg = f"You have successfully lookup the {prefix}routine list."
    return msg