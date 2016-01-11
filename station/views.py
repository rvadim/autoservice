from rest_framework import viewsets

from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

from station.models import Station
from station.models import Service
from station.models import Job
from station.models import Client
from station.models import Car
from station.models import Stand
from station.models import generate_username

from station.serializers import StationSerializer
from station.serializers import ServiceSerializer
from station.serializers import JobSerializer

import datetime
from dateutil import tz

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

    @staticmethod
    def _find_client(phone):
        clients = Client.objects.filter(phone__exact=phone)
        if len(clients) == 0:
            return None
        return clients[0]

    @staticmethod
    def _validate_phone(phone_str):
        if phone_str is not None:
            return phone_str.replace(' ', '').replace('-', '')
        raise ValidationError(_('Phone number is invalid'))

    @staticmethod
    def _validate_client(client):
        if 'phone' in client and 'car' in client:
            return client
        raise ValidationError(_('Client in you request have '
                                'not phone and/or car'))

    @staticmethod
    def _validate_car(car):
        if 'manufacturer' in car and 'model' in car:
            return car
        raise ValidationError(_('Car in you request have not '
                                'manufacturer and/or model'))

    @staticmethod
    def _validate_data(data):
        if 'client' in data and 'date' in data and 'selected_services' in data:
            return data
        raise ValidationError(_('Not all parameters found in request, '
                                'should presents: client, date and '
                                'selected_services'))

    @staticmethod
    def _validate_datetime(date_time):
        DATETIME_FORMAT='%Y-%m-%dT%H:%M:%S.%fZ'
        try:
            date = datetime.datetime.strptime(date_time, DATETIME_FORMAT)
            date = date.replace(tzinfo=tz.tzutc())
            date = date.replace(second=0, microsecond=0)
            return date
        except ValueError as e:
            raise ValidationError(_('Date of request format is invalid, '
                                    '{}'.format(e)))

    @staticmethod
    def _validate_services(services):
        return services

    @staticmethod
    def _get_services_time(services_ids):
        output = None
        services = Service.objects.filter(id__in=services_ids)
        if len(services) != len(services_ids):
            raise ValidationError('Not all services found, search for '
                                  'ids {}, found {}'.format(services_ids,
                                                            services))
        for service in services:
            if output is None:
                output = service.min_duration
            else:
                output += service.min_duration
        return output

    def create(self, request, *args, **kwargs):
        log.debug('Data from request: {}'.format(request.data))
        data = self._validate_data(request.data)
        client = self._validate_client(data.get('client', {}))
        phone = self._validate_phone(client.get('phone', None))
        car = self._validate_car(client.get('car', {}))
        c = self._find_client(phone)
        if c is None:
            c = Client()
            user = User(username=generate_username())
            user.save()
            c.user = user
            c.phone = phone
        car = Car(manufacturer=car.get('manufacturer'),
                  model=car.get('model'))
        car.save()
        c.car = car
        c.save()
        proper_data = {
            'client': c.id,
            'services': self._validate_services(data.get('selected_services')),
            'stand': None,
            'date_time': self._validate_datetime(data.get('date'))
        }
        delta = self._get_services_time(proper_data.get('services'))
        log.debug('Search for '
                  'overlaps of: {} - {}'.format(
                    proper_data.get('date_time'),
                    proper_data.get('date_time') + delta))

        log.debug('All jobs: %s', Job.objects.all())
        jobs = Job.objects\
            .filter(date_time__gte=proper_data.get('date_time')) \
            .filter(date_time__lte=proper_data.get('date_time') + delta)
        log.debug('Jobs overlaps: %s', jobs)
        stands = Stand.objects.all()
        log.debug('All stands: %s', stands)
        for stand in stands:
            busy = False
            for job in jobs:
                if job.stand.id == stand.id:
                    busy = True
            if not busy:
                proper_data['stand'] = stand.id
        if proper_data.get('stand') is None:
            return Response({'detail': _('No free stands for accept job')},
                            status=status.HTTP_409_CONFLICT)

        log.debug('Final data for create job: {}'.format(proper_data))
        serializer = self.get_serializer(data=proper_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)
