import stripe
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse


class UserChangedPasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and \
                not request.user.has_changed_password:
            if not request.path.startswith(reverse('edit_password')):
                return render(request, 'user/change_password.html', {})
        response = self.get_response(request)
        return response


class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            if not request.path.startswith(reverse('checkout')):
                if request.user.stripe_subscription_id is None:
                    return redirect('checkout')
                else:
                    subscription = stripe.Subscription.retrieve(
                        request.user.stripe_subscription_id
                    )
                    print(subscription)
                    if subscription.status != 'active':
                        return redirect('https://buy.stripe.com/test_4gweV8a6fcKVcggcMM')
                    else:
                        HttpResponse("Success")

        response = self.get_response(request)
        return response
