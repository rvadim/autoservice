from django.apps import AppConfig
from django.utils.translation import ugettext as _


class StationConfig(AppConfig):
    name = 'station'
    verbose_name = _('Station')
