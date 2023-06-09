from django.shortcuts import render
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