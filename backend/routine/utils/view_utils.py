from ..models import RoutineResult

def logical_delete_routine_result(instance):
    result = RoutineResult.objects.get(routine=instance.id)
    result.is_deleted = True
    result.save()

def logical_delete_routine(instance):
    instance.is_deleted = True
    instance.save()
    logical_delete_routine_result(instance)