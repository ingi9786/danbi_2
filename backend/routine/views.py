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

# retreive, update, delete
class RoutineDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data":   {"account_id": self.request.user.id,
                                    "routine_id": serializer.data},
                        "message": {"msg":"You have successfully lookup the routine.",
                                    "status": "ROUTINE_LOOKUP_OK"}})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(rid=instance.id)
            return Response({"data":    {"routine_id": serializer.data.get('id', None)}, 
                             "message": {"msg":"You have successfully updated the routine.",
                                         "status": "ROUTINE_UPDATE_OK"}})

Routine_update_view = RoutineDetailAPIView.as_view()