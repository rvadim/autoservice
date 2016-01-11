from django.test import TestCase
from django.contrib.auth.models import User

from station.models import Station, Box, Stand, Service, Job

import logging
import datetime
import json

log = logging.getLogger(__name__)


class AbstractEntityApiTestCase(TestCase):
    allowed_codes = [200, 201, 400, 403, 404, 409, 415, ]

    user_login = 'user'
    user_plain_password = 'qweqwe'

    def setUp(self):
        User.objects.create_user(username=self.user_login,
                                 email='user@domain.tld',
                                 password=self.user_plain_password)
        self.client.login(username=self.user_login,
                          password=self.user_plain_password)

    def _call_rest(self, method, url,
                   data=None, content_type='application/json'):
        http_method = getattr(self.client, method)
        url = '/{0}/{1}'.format('api', url)
        request_data = None
        if data is not None:
            if content_type == 'application/json':
                request_data = json.dumps(data)
            else:
                request_data = data

        response = http_method(url,
                               data=request_data,
                               content_type=content_type)

        if response.status_code not in self.allowed_codes:
            raise IndexError('HTTP status code {0} out of range '
                             'of expected values.'.
                             format(response.status_code))

        if not response.content:
            return response

        if content_type == u'application/json':
            return json.loads(response.content.decode('utf-8',
                                                      errors='replace'))
        else:
            return response


class JobTests(AbstractEntityApiTestCase):

    def setUp(self):
        self.station = Station(name='MyTestStation')
        self.station.save()
        self.box = Box(station=self.station, address='My address str. 4')
        self.box.save()
        self.stand = Stand(box=self.box, name='MyStand')
        self.stand.save()
        self.service = Service(name='TestService',
                               min_duration=datetime.timedelta(minutes=30),
                               max_duration=datetime.timedelta(minutes=30),
                               min_cost=500,
                               max_cost=1000)
        self.service.save()

    def tearDown(self):
        self.station.delete()
        self.box.delete()
        self.stand.delete()
        self.service.delete()

    def _create_job(self, client, services, date_time):
        data = {
            'client': client,
            'selected_services': services,
            'date': date_time
        }
        return self._call_rest('post', 'job/', data)

    def test_job_creation(self):
        selected_services = [1, 2]
        date = '2016-01-11T03:00:07.451Z'
        client = {
            'phone': '8 999 000 0000',
            'car': {'model': 'Impreza', 'manufacturer': 'Subaru'}
        }

        job = self._create_job(client, selected_services, date)
        self.assertEqual(job.get('client'), 1)
        self.assertEqual(job.get('stand'), 1)
        self.assertEqual(job.get('date_time'), '2016-01-11T03:00:07.451000Z')

    def test_job_not_assigned_to_one_time(self):
        selected_services = [1]
        date1 = '2016-01-11T03:00:07.451Z'
        client = {
            'phone': '8-100-000-0000',
            'car': {'model': 'Impreza', 'manufacturer': 'Subaru'}
        }
        date2 = '2016-01-11T03:00:00.000Z'
        date3 = '2016-01-11T02:59:00.000Z'

        job = self._create_job(client, selected_services, date1)
        self.assertEqual(job['stand'], self.stand.id)
        job = self._create_job(client, selected_services, date2)
        self.assertEqual(job['detail'], 'No free stands for accept job')
        job = self._create_job(client, selected_services, date3)
        log.warn(job)

