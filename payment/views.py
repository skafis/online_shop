# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from orders.models import Order

# Create your views here.
def payment_process(request):
	order_id = request.session.get('order_id')
	order = get_object_or_404(Order, id=order_id)
	host = request.get_host()

	paypal_dict = {
		'business': settings.PAYPAL_RECIEVER_EMAIL,
		'amount': '%.2f' % order.get_cost().quantize(
												Decimal('.01')),
		'invoice' : str(order.id),
		'currency_code' : 'USD',
		'notify_url' : 'http://{}{}'.format(host,
											reverse('paypal-ipn')),
		'return_url' : 'http://{}{}'.format(host, 
											reverse('payment:done')),
		'cancel_return': 'http://{}{}'.format(host,
											reverse('payment:canceled')),
	}
	form = PayPalPaymentsForm(initial=paypal_dict)
	ctx = {
		'order': order,
		'form' : form,
	}
	return render(request,
					'payment/process.html',
					ctx)

@csrf_exempt
def payment_done(request):
	return render(request, 'payment/done.html')

@csrf_exempt
def payment_canceled(request):
	return render(request, 'payment/canceled.html')