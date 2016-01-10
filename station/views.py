from rest_framework import viewsets

from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework import status

from station.models import Station
from station.models import Service
from station.models import Job

from station.serializers import StationSerializer
from station.serializers import ServiceSerializer
from station.serializers import JobSerializer

import logging
log = logging.getLogger(__name__)


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def create(self, request, *args, **kwargs):
        log.info(request.data)
        return Response({}, status=status.HTTP_201_CREATED)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

