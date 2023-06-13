import datetime
import logging
from multiprocessing import Process

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST, require_GET

from authentication.models import User
from authentication.utils import send_registration_mail
from project.models import Project


# Create your views here.
def handler404(request, *args, **argv):
    response = render(request, "utils/404.html", {})
    response.status_code = 404
    return response


def handler401(request, *args, **argv):
    response = render(request, "utils/404.html", {})
    response.status_code = 401
    return response


@require_POST
def save_user(request):
    form_user = request.POST
    name = form_user.get("name")
    email = form_user.get("email")
    password1 = form_user.get("password1")
    password2 = form_user.get("password2")
    if password1 == password2:
        User = get_user_model()
        user = User.objects.create_user(
            email=email, password=password1, username=name
        )
        user.save()
        messages.success(
            request, "Registered successfully! Login to continue."
        )
    else:
        messages.error(request, "Passwords do not match")
    return render(request, "user/login.html", {})


@require_POST
def validate_user(request):
    if request.user.is_authenticated:
        return redirect("home")
    current_user = request.POST
    email = current_user.get("email")
    password = current_user.get("password")
    user = authenticate(email=email, password=password)
    if user is not None:
        login(request, user)
        return redirect("home")
    else:
        messages.error(request, "Invalid username or password")
    return render(request, "user/login.html", {})


@require_POST
@login_required
def edit_user(request):
    form_user = request.POST
    user_id = form_user.get("user_id")
    username = form_user.get("username")
    firstname, lastname = form_user.get("fullname").split()
    profile_picture = request.FILES.get("profile_picture")
    remove_profile = form_user.get("remove_profile")
    about = form_user.get("about")
    contact_no = form_user.get("contact_no")
    current_user = User.objects.get(id=user_id)
    current_user.id = user_id
    current_user.username = username
    current_user.firstname = firstname
    current_user.lastname = lastname
    if remove_profile == "on":
        current_user.image = "profiles/default.png"
    elif profile_picture is None:
        current_user.image = current_user.image
    else:
        current_user.image = profile_picture
    current_user.about = about
    current_user.contact_no = contact_no
    current_user.save()
    return redirect("profile")


@require_POST
@login_required
def edit_password(request):
    form_user = request.POST
    user_id = form_user.get("user_id_reset")
    current_password = form_user.get("current_password")
    new_password = form_user.get("new_password")
    new_password_again = form_user.get("new_password_again")
    current_user = User.objects.get(id=user_id)
    if current_password is None:
        current_user.set_password(new_password)
        current_user.has_changed_password = True
        current_user.save()
        login(request, current_user)
        messages.success(request, "Passwords changed successfully.")
    else:
        if current_user.check_password(current_password):
            if new_password == new_password_again:
                current_user.set_password(new_password)
                current_user.save()
                login(request, current_user)
                messages.success(request, "Passwords changed successfully.")
            else:
                messages.error(request, "Passwords do not match")
        else:
            messages.error(request, "Wrong password")
    return redirect("profile")


@require_GET
@login_required
def view_company_users(request, page_no):
    logging.info(f'Viewing company users {request.GET}')
    context = {}
    current_user = request.user
    company_users = User.objects.filter(
        Q(company=current_user.company) &
        Q(is_owner=False)).exclude(Q(is_superuser=True) |
                                   Q(is_active=False) |
                                   Q(company=None)).order_by(
        'username', 'date_joined')
    projects = Project.objects.filter(
        Q(is_deleted=False) &
        Q(created_by__company=current_user.company)
    )
    context["projects"] = projects
    paginator = Paginator(company_users, 6)
    page_obj = paginator.get_page(page_no)
    context["ELLIPSIS"] = page_obj.paginator.ELLIPSIS
    context["page_obj"] = page_obj.object_list
    context["has_next"] = page_obj.has_next()
    if context["has_next"]:
        context["next_page_no"] = page_obj.next_page_number()
    else:
        context["next_page_no"] = 1
    context["has_previous"] = page_obj.has_previous()
    if context["has_previous"]:
        context["previous_page_no"] = page_obj.previous_page_number()
    else:
        context["previous_page_no"] = 1
    context["last_page"] = page_obj.paginator.num_pages
    context["elided_pages"] = paginator.get_elided_page_range(
        page_no, on_each_side=1, on_ends=2
    )
    context["current_page"] = page_obj.number
    return render(request, "company/company.html", context)


@require_POST
@login_required
def add_company_users(request):
    response = redirect('view_users', page_no=1)
    email = request.POST.get('email')
    if email is not None:
        email = email.lower()
    else:
        messages.error(request, "Please enter your email address")
        return response
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    project = request.POST.getlist('projects')
    user = User.objects.filter(email=email).first()
    if user is not None and user.is_active:
        messages.error(request, "User with given email already exists.")
        return response
    elif user is not None:
        password = User.objects.make_random_password()
        user.set_password(password)
        user.has_changed_password = False
        user.is_active = True
        user.date_joined = datetime.datetime.now()
    else:
        username = email.split("@")[0]
        password = User.objects.make_random_password()
        user = User.objects.create_user(
            email=email,
            password=password,
            username=username
        )
    user.company = request.user.company
    user.firstname = firstname
    user.lastname = lastname
    user.save()
    for project_id in project:
        projects = Project.objects.get(id=project_id)
        projects.assign.add(User.objects.get(email=user.email))
    uri = request.build_absolute_uri('/')[:-1]
    email_process = Process(
        target=send_registration_mail,
        args=(user.email, password, user.firstname, str(user.company), uri)
    )
    email_process.start()
    return response


def search_company_users(request):
    query = request.GET.get('query')
    page_no = request.GET.get("page_no")
    if page_no == "undefined":
        page_no = 1
    context = {}
    current_user = request.user
    company_users = User.objects.filter(
        Q(company=current_user.company) &
        Q(is_owner=False) &
        Q(is_active=True)).exclude(is_superuser=True).order_by('username',
                                                               'date_joined')
    if query is not None:
        company_users = company_users.filter(
            Q(firstname__icontains=query) | Q(lastname__icontains=query))
    company_users = list(
        company_users.extra(
            select={'raw_phone': 'authentication_user.contact_no'}).
        values('pk', 'firstname', 'lastname', 'email',
               'raw_phone', 'date_joined'))
    paginator = Paginator(company_users, 10)
    page_obj = paginator.get_page(page_no)
    context["page_obj"] = list(page_obj.object_list)
    context["has_next"] = page_obj.has_next()
    if context["has_next"]:
        context["next_page_no"] = page_obj.next_page_number()
    else:
        context["next_page_no"] = 1
    context["has_previous"] = page_obj.has_previous()
    if context["has_previous"]:
        context["previous_page_no"] = page_obj.previous_page_number()
    else:
        context["previous_page_no"] = 1
    context["last_page"] = page_obj.paginator.num_pages
    context["current_page"] = page_obj.number
    return JsonResponse(context, safe=False)


@login_required
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    projects = Project.objects.filter(is_deleted=False)
    for project in projects:
        if project.assign.filter(id=user.id).exists():
            project.assign.remove(user)
    user.is_active = False
    user.save()
    return redirect("view_users", page_no=1)
