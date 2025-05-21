from django.shortcuts import render
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from .models import StripePayment
import json

stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(APIView):
    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(float(request.data['amount']) * 100),  # amount in cents
                        'product_data': {
                            'name': request.data['product_name'],
                        },
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f"{settings.DOMAIN_URL}/payment-success?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url=f"{settings.DOMAIN_URL}/payment-cancelled",
            )
            return Response({'sessionId': checkout_session.id})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = 'your_webhook_secret_here'

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']

            StripePayment.objects.create(
                stripe_session_id=session['id'],
                email=session.get('customer_email', ''),
                amount=int(session['amount_total']) / 100,
                currency=session['currency'],
                status=session['payment_status']
            )

        return HttpResponse(status=200)