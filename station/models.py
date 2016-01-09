from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class Station(models.Model):
    name = models.CharField(_('Name'), max_length=128, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Station')
        verbose_name_plural = _('Stations')


class Box(models.Model):
    station = models.ForeignKey('Station')
    address = models.CharField(_('Address'), max_length=255)

    def __str__(self):
        return '{} -> {}'.format(self.station.name, self.address)

    class Meta:
        verbose_name = _('Box')
        verbose_name_plural = _('Boxes')


class Stand(models.Model):
    box = models.ForeignKey('Box')
    name = models.CharField(_('Name'), max_length=128, unique=True)

    def __str__(self):
        return '{} -> {}'.format(self.box.address, self.name)

    class Meta:
        verbose_name = _('Stand')
        verbose_name_plural = _('Stands')


class Service(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    min_cost = models.PositiveIntegerField(_('Min. cost'))
    max_cost = models.PositiveIntegerField(_('Max. cost'))
    min_duration = models.DurationField(_('Min. duration'))
    max_duration = models.DurationField(_('Max. duration'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Service')
        verbose_name_plural = _('Services')


class Client(models.Model):
    user = models.ForeignKey(User)
    phone = models.CharField(_('Cell phone'), max_length=12)

    def __str__(self):
        return '{} {}, {}'.format(self.user.last_name, self.user.first_name,
                                  self.phone)

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')


class Job(models.Model):
    client = models.ForeignKey('Client')
    services = models.ManyToManyField('Service')
    stand = models.ForeignKey('Stand')
    date_time = models.DateTimeField(_('Arrival time'))
    approved = models.BooleanField(_('Approved'), default=False)
    completed = models.BooleanField(_('Completed'), default=False)

    def __str__(self):
        return '{}, {}, {}'.format(self.client, self.services, self.date_time)

    def get_services(self):
        return ','.join([service.name for service in self.services.all()])

    class Meta:
        verbose_name = _('Job')
        verbose_name_plural = _('Jobs')


def generate_services(count):
    import random
    import string
    from datetime import timedelta
    for i in range(0, count):
        service = Service()
        service.name = ''.join(random.SystemRandom().choice(
            string.ascii_uppercase + string.digits) for _ in range(16))
        service.min_cost = random.randint(100, 500)
        service.max_cost = random.randint(500, 5000)
        service.min_duration = timedelta(seconds=random.randint(600, 1200))
        service.max_duration = timedelta(seconds=random.randint(1200, 60000))
        service.save()

