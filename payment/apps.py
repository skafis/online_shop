# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class PaymentConfig(AppConfig):
    name = 'payment'
    verbose_name = 'payment'

    def ready(self):
    	# import signal handlers
    	import payment.signals
