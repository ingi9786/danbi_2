from rest_framework.response import Response
from rest_framework import generics, mixins

from .models import Routine, RoutineDay, RoutineResult
from .serializers import RoutineSerializer, RoutineDaySerializer, RoutineResultSerializer


 
# create
class RoutineListCreateAPIView(generics.ListCreateAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = RoutineSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(uid=user.id)
            return Response({"data":    {"routine_id": serializer.data.get('id', None)}, 
                             "message": {"msg":"You have successfully created the routine.",
                                         "status": "ROUTINE_CREATE_OK"}})

Routine_list_create_view = RoutineListCreateAPIView.as_view()

# update
class RoutineUpdateAPIView(generics.UpdateAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(rid=instance.id)
            return Response({"data":    {"routine_id": serializer.data.get('id', None)}, 
                             "message": {"msg":"You have successfully updated the routine.",
                                         "status": "ROUTINE_UPDATE_OK"}})

Routine_update_view = RoutineUpdateAPIView.as_view()