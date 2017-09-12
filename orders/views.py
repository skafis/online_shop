# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import weasyprint

from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse 
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

# Create your views here.
def order_create(request):
	cart = Cart(request)
	if request.method == 'POST':
		form =OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order=order,
										product=item['product'],
										price=item['price'],
										quantity=item['quantity']
										)
			# clear the cart
			cart.clear()
			# launch asynchronus task
			order_created.delay(order.id) #set the oder in the session
			request.session['order_id'] = order.id #Redirect to payment
			return redirect(reverse('payment:process'))
		# return render(request,
		# 				'orders/order/created.html',{'order': order})
		
	else:
		form = OrderCreateForm()
	
	return render(request,
					'orders/order/create.html',
					{'cart': cart, 'form': form})

@staff_member_required
def admin_order_detail(request, oder_id):
	order = get_object_or_404(Order, id=oder_id)
	html = render_to_string('orders/order/pdf.html',{'order':order})
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] - 'filename=\
			"order_{}.pdf"'.format(order.id)
	weasyprint.HTML(string=html).write_pdf(reaponse,
		stylesheets=[weasyprint.css(
			settings.STATIC_ROOT+'css/pdf.css')])
	
	return response


	return render(request, 
					'admin/orders/order/detail.html',
					{'order': order})