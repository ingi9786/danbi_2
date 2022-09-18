from .models import Routine
from .utils.mixins_utils import *



class ListQuerySetMixin():
    def get_queryset(self):
        date = self.request.GET.get('date', None)
        isdel = self.request.GET.get('is-del', None)

        uid = self.request.user.id
        qs = Routine.objects.filter(account=uid)
        
        # 삭제되지 않은 routine 보여주기 
        if (date is None) and (bool(isdel)==0):
            return qs.filter(is_deleted=False)
        # 삭제된 routine 보여주기
        elif (date is None) and (bool(isdel)==1):
            return qs.filter(is_deleted=True)
        elif date is not None:
            day = convert_day(date) if is_valid_date(date) else get_today()
            if bool(isdel)==0:
                return qs.filter(is_deleted=False, routineday__day=day)
            else:
                return qs.filter(is_deleted=True, routineday__day=day)

        return qs
    
# date delete
#  0     0     모든 살아있는 routine
#  0     1     모든 죽어있는 routine
#  1     0     특정 날짜에 삭제되지 않은 routine
#  1     1     특정 날짜에 삭제된 routine (내가 몇일에 삭제했는지가 필요할지 모르지만 구현)