from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Routine, RoutineDay, RoutineResult
from .serializers import RoutineSerializer, RoutineDaySerializer, RoutineResultSerializer
from .utils import view_utils


# List view
class RoutineListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = RoutineSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self):
        uid = self.request.user.id
        queryset = Routine.objects.filter(account=uid, is_deleted=False)
        return queryset
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = RoutineSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(uid=user.id)
            return Response({"data":    {"routine_id": serializer.data.get('id', None)}, 
                             "message": {"msg":"You have successfully created the routine.",
                                         "status": "ROUTINE_CREATE_OK"}})
 
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return  Response({"data":     serializer.data, 
                          "message": {"msg":"You have successfully lookup the routines.",
                                      "status": "ROUTINE_LIST_OK"}})


# Detail view
class RoutineDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self):
        uid = self.request.user.id
        queryset = Routine.objects.filter(account=uid, is_deleted=False)
        return queryset
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data":   {"account_id": self.request.user.id,
                                    "routine_id": serializer.data},
                        "message": {"msg":"You have successfully lookup the routine.",
                                    "status": "ROUTINE_DETAIL_OK"}})

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(rid=instance.id)
            return Response({"data":    {"routine_id": serializer.data.get('id', None)}, 
                             "message": {"msg":"You have successfully updated the routine.",
                                         "status": "ROUTINE_UPDATE_OK"}})
            
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        view_utils.logical_delete_routine(instance)
        return Response({"data":    {"routine_id": instance.id}, 
                         "message": {"msg":"You have successfully deleted the routine.",
                                     "status": "ROUTINE_DELETE_OK"}})


class DeletedRoutineListAPIView(generics.ListAPIView):
    serializer_class = RoutineSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self):
        uid = self.request.user.id
        queryset = Routine.objects.filter(account=uid, is_deleted=True)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return  Response({"data":     serializer.data, 
                          "message": {"msg":"You have successfully lookup the deleted routines.",
                                      "status": "DELETED_ROUTINE_LIST_OK"}})


class DatedRoutineListAPIView(generics.ListAPIView):
    serializer_class = RoutineSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self):
        date = self.request.GET.get('date', 'None')

        if view_utils.is_valid_date(date):
            day = view_utils.convert_day(date)
        else:
            day = view_utils.get_today()
        
        uid = self.request.user.id
        queryset = Routine.objects.filter(account=uid, is_deleted=False, routineday__day=day)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return  Response({"data":     serializer.data, 
                          "message": {"msg":"You have successfully lookup the routines.",
                                      "status": "ROUTINE_DATE_LIST_OK"}})


Routine_list_create_view = RoutineListCreateAPIView.as_view()
Routine_detail_view = RoutineDetailAPIView.as_view()
Deleted_routine_list_view = DeletedRoutineListAPIView.as_view()
Dated_Routine_list_view = DatedRoutineListAPIView.as_view()