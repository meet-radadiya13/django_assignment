import stripe
from django.shortcuts import redirect, render
from django.urls import reverse


class UserChangedPasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and \
                not request.user.has_changed_password and not request.user.is_superuser:
            if not request.path.startswith(reverse('create_password')):
                return render(request, 'user/change_password.html', {})
        response = self.get_response(request)
        return response


class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_superuser:
            if not request.path.startswith(reverse('checkout')):
                if request.user.stripe_subscription_id is None:
                    return redirect('checkout')
                subscription = stripe.Subscription.retrieve(
                    request.user.stripe_subscription_id
                )
                if subscription.status != 'active':
                    return redirect('checkout')

        response = self.get_response(request)
        return response
