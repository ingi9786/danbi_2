from .models import Routine
from .utils.mixins_utils import *


# 쿼리 파람은 str False, True. 
class ListQuerySetMixin():
    def get_queryset(self):
        date = self.request.GET.get('date', None)
        is_del = self.request.GET.get('is-del', None)
        if is_del==None or is_del=='0':
            is_del = False
        else:
            is_del = True
        
        uid = self.request.user.id
        if is_del==False:
            qs = Routine.objects.filter(account=uid, is_deleted=False)
        else:
            del_qs = Routine.del_objects.filter(account=uid)
            return del_qs
        
        if date is None:
            return qs
        elif date is not None:
            day = convert_day(date) if is_valid_date(date) else get_today()
            return qs.filter(routineday__day=day)