from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Routine, RoutineDay, RoutineResult


class RoutineDaySerializer(serializers.ModelSerializer):
    class Meta:
        model            = RoutineDay
        fields           = "__all__"
        read_only_fields = ('routine', 'created_at', 'modified_at', )


class RoutineResultSerializer(serializers.ModelSerializer):
    class Meta:
        model            = RoutineResult
        fields           = "__all__"
        read_only_fields = ('id', 'routine', 'is_delete', 'created_at', 'modified_at',)


class RoutineSerializer(serializers.ModelSerializer):
    days = RoutineDaySerializer(many=True)

    class Meta:
        model            = Routine
        fields           = "__all__"
        read_only_fields = ('id', 'account', 'is_delete', 'created_at', 'modified_at',)
        
    def create(self, validated_data):
        # validated_data = {days': [OrderedDict([('day', 'mon')])], 'title': ... , 'uid':1} 
        days = validated_data.pop('days')

        # routine 생성 
        uid = validated_data.pop('uid')
        db = get_user_model()
        userobj = db.objects.get(id=uid)
        routine = Routine.objects.create(**validated_data, account=userobj)
        
        # routine day 생성
        for day in days:
            RoutineDay.objects.create(**day, routine=routine)
        
        # routine result 생성
        RoutineResult.objects.create(routine=routine)
        return routine 


# inner serializer가 validate를 수행한다. 대신 json 입력이 "days": [{'day':'mon'}, {'day':'tue'}] 이다. 
# Advance: json 입력을 "days":["mon", "tue"]로 할수 없나? 