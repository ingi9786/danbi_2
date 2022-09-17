from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Routine, RoutineDay, RoutineResult


class RoutineDaySerializer(serializers.ModelSerializer):
    class Meta:
        model            = RoutineDay
        fields           = ['day', ]


class RoutineResultSerializer(serializers.ModelSerializer):
    class Meta:
        model            = RoutineResult
        fields           = ['result', ]


class RoutineSerializer(serializers.ModelSerializer):
    days = RoutineDaySerializer(many=True)
    result = RoutineResultSerializer(many=True)

    class Meta:
        model            = Routine
        fields           = ['id', 'account', 'title', 'category', 'goal', 'is_alarm','days', 'result']
        read_only_fields = ('id', 'account', 'is_delete')
        
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


    def update(self, instance, validated_data):
        days = validated_data.pop('days')
    
        # routine 수정
        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        # routine day
        rid = validated_data.get('rid')
        day_qs = RoutineDay.objects.filter(routine_id=rid)
        existing_days = set([day_q.day for day_q in day_qs])
        new_days      = set([day['day'] for day in days])

        days_will_be_delete = existing_days.difference(new_days)
        days_will_be_create = new_days.difference(existing_days)
        
        if days_will_be_delete:
            for day in days_will_be_delete:
                RoutineDay.objects.get(routine_id=rid, day=day).delete()

        if days_will_be_create:
            routine = Routine.objects.filter(id=rid).first()
            for day in days_will_be_create:
                RoutineDay.objects.create(routine=routine, day=day)
                
        return instance
