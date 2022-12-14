from rest_framework.response import Response
from rest_framework import generics, mixins
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Routine, RoutineDay, RoutineResult
from .serializers import RoutineSerializer, RoutineDaySerializer, RoutineResultSerializer
from .utils import view_utils
from .mixins import ListQuerySetMixin



# List view
class RoutineListCreateAPIView(ListQuerySetMixin, generics.ListCreateAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = RoutineSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(uid=user.id)
            return Response({"data":{"routine_id": serializer.data.get('id', None)},
                             "message": "You have successfully created the routine.",
                             "status": status.HTTP_201_CREATED
                            })
 
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        if not queryset.exists():
            return Response({"message": "There is no routine.",
                             "status": status.HTTP_204_NO_CONTENT
                            })
        
        serializer = self.get_serializer(queryset, many=True)
        msg = view_utils.get_LIST_response_msg(request)
        return  Response({"data": serializer.data,
                          "message": msg,
                          "status": status.HTTP_200_OK
                        })

# Detail view
class RoutineDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    
    def get_queryset(self):
        uid = self.request.user.id
        queryset = Routine.objects.filter(account=uid)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data":{"account_id": self.request.user.id,
                                 "routine_id": serializer.data},
                        "message": "You have successfully lookup the routine.",
                        "status": status.HTTP_200_OK
                        })

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
    
        if serializer.is_valid(raise_exception=True):
            serializer.save(rid=instance.id)
            return Response({"data": {"routine_id": serializer.data.get('id', None)}, 
                             "message": "You have successfully updated the routine.",
                             "status": status.HTTP_200_OK
                            })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        view_utils.logical_delete_routine(instance)

        return Response({"data":{"routine_id": instance.id}, 
                         "message": "You have successfully deleted the routine.",
                         "status": status.HTTP_200_OK
                        })


class DeletedRoutineMixinView(mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    generics.GenericAPIView):
    
    queryset = Routine.del_objects.all()
    serializer_class = RoutineSerializer
    authentication_classes = (SessionAuthentication, )
    permission_classes = (IsAuthenticated, )
    lookup_field = 'pk'
    
    def get(self, request, *args, **kwargs): #HTTP -> get
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data":{"account_id": self.request.user.id,
                                 "routine_id": serializer.data},
                        "message": "You have successfully lookup the deleted routine.",
                        "status": status.HTTP_200_OK
                        })

    def perform_update(self, serializer, **kwargs):
        serializer.save(restore=True)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
    
        if serializer.is_valid(raise_exception=True):
            self.perform_update(serializer)
            return Response({"data": {"routine_id": serializer.data.get('id', None)}, 
                             "message": "You have successfully restored the routine.",
                             "status": status.HTTP_200_OK
                            })

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        if not queryset.exists():
            return Response({"message": "There is no deleted routine.",
                             "status": status.HTTP_204_NO_CONTENT
                            })
        
        serializer = self.get_serializer(queryset, many=True)
        return  Response({"data": serializer.data,
                          "message": "You have successfully lookup the deleted routine list",
                          "status": status.HTTP_200_OK
                        })

Routine_list_create_view = RoutineListCreateAPIView.as_view()
Routine_detail_view = RoutineDetailAPIView.as_view()
Deleted_routine_mixin_view = DeletedRoutineMixinView.as_view()
