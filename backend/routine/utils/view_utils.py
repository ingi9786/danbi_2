from ..models import Routine, RoutineResult



def logical_delete_routine(routine):
    routine.soft_delete()
    result = RoutineResult.objects.get(routine=routine)
    result.soft_delete()

def get_LIST_response_msg(request):
    date    = bool(request.GET.get('date', None))

    prefix = ''
    if date==False:
        prefix = ''
    elif date==True:
        prefix = 'DATED '

    msg = f"You have successfully lookup the {prefix}routine list."
    return msg