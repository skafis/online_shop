import weasyprint 

from django.shortcuts import get_object_or_404
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from io import BytesIO

from orders.models import Order

def payment_notification(sender, **kwargs):
	ipn_obj = sender
	if ipn_obj.payment_status == ST_PP_COMPLETED:
		# payment was successful
		order = get_object_or_404(Order, id=ipn_obj.invoice)

		# mark order as paid
		order.paid = True
		order.save()

		# crreate invoice e-mail
		subject = 'My shop - invoice no. {}'.format(order.id)
		message = 'please find attached the invoice for yor recent purchase'
		email = EmailMessage(subject,
							message,
							'admin@myshop.com'
							[order.email])
		# generate pdf
		html = render_to_string('oders/order/pdf.html',{'order':order})
		out= BytesIO()
		stylesheets = [weasyprint.css(settings.STATIC_ROOT+'css/pdf.css')]
		weasyprint.HTML(string=html).write_pdf(out,
												stylesheets=stylesheets)
		# attach a pdf
		email.attach('order_{}.pdf'.format(order.id),
						out.getvalue(),
						'application/pdf')

		# send email
		email.send()


valid_ipn_received.connect(payment_notification)

