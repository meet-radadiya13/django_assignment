from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from authentication.models import User


# Create your views here.
def handler404(request, *args, **argv):
    response = render(request, "utils/404.html", {})
    response.status_code = 404
    return response


@require_POST
def save_user(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")
    if password1 == password2:
        User = get_user_model()
        user = User.objects.create_user(email=email, password=password1, username=name)
        user.save()
    else:
        messages.error(request, "Passwords do not match")
    return render(request, "user/login.html", {})


@require_POST
def validate_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
        return render(request, "user/login.html", {})


@login_required
@require_POST
def edit_user(request):
    user_id = request.POST.get("user_id")
    username = request.POST.get("username")
    firstname, lastname = request.POST.get("fullname").split()
    profile_picture = request.FILES.get("profile_picture")
    remove_profile = request.POST.get("remove_profile")
    about = request.POST.get("about")
    contact_no = request.POST.get("contact_no")

    user = User()
    current_user = User.objects.get(id=user_id)
    user.id = user_id
    user.username = username
    user.password = current_user.password
    user.date_joined = current_user.date_joined
    user.email = current_user.email
    user.firstname = firstname
    user.lastname = lastname

    if remove_profile == "on":
        user.image = "profiles/default.png"
    elif profile_picture is None:
        user.image = current_user.image
    else:
        user.image = profile_picture

    user.about = about
    user.contact_no = contact_no

    user.save()

    return redirect("profile")


@login_required
@require_POST
def edit_password(request):
    user_id = request.POST.get("user_id_reset")
    current_password = request.POST.get("current_password")
    new_password = request.POST.get("new_password")
    new_password_again = request.POST.get("new_password_again")

    current_user = User.objects.get(id=user_id)
    if current_user.check_password(current_password):
        if new_password == new_password_again:
            current_user.set_password(new_password)
            current_user.save()
        else:
            messages.error(request, "Passwords do not match")
    else:
        messages.error(request, "Wrong password")
    return redirect("profile")
