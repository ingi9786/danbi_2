from .models import Routine
from .utils.mixins_utils import *


# 쿼리 파람은 str False, True. 
class ListQuerySetMixin():
    def get_queryset(self):
        date = self.request.GET.get('date', None)
        uid = self.request.user.id
        qs = Routine.objects.filter(account=uid, is_deleted=False)
        
        if date is None:
            return qs
        elif date is not None:
            day = convert_day(date) if is_valid_date(date) else get_today()
            return qs.filter(routineday__day=day)