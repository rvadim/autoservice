from rest_framework import viewsets

from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from station.models import Station
from station.models import Service
from station.models import Job

from station.serializers import StationSerializer
from station.serializers import ServiceSerializer
from station.serializers import JobSerializer


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

