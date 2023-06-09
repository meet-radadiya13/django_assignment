import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from authentication.models import User
from project.models import Project


# Create your views here.
@login_required
def view_projects(request, page_no):
    current_user = request.user
    my_projects = Project.objects.filter(
        Q(created_by=current_user) | Q(assign=current_user)
    ).exclude(is_deleted=True)
    context = {}
    paginator = Paginator(my_projects, 6)
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
    return render(request, "project/project.html", context)


@login_required
def add_projects(request):
    users = User.objects.exclude(
        Q(username=request.user.username) | Q(is_superuser=True)
    ).exclude(is_active=False)
    context = {"users": users}
    return render(request, "project/add_project.html", context)


@login_required
@require_POST
def insert_projects(request):
    project_name = request.POST.get("project_name")
    project_acronym = request.POST.get("project_acronym")
    project_assignee = request.POST.getlist("assignee")
    dead_line = request.POST.get("dead_line")
    tags = request.POST.getlist("tags")
    project_description = request.POST.get("project_desc")
    completed = request.POST.get("completed")
    project = Project()
    users = []
    for user in project_assignee:
        users.append(User.objects.filter(username=user))
    project.name = project_name
    project.acronym = project_acronym
    year, month, date = dead_line.split("-")
    _dead_line = datetime.date(int(year), int(month), int(date))
    project.dead_line = _dead_line
    project.tags = tags
    project.description = project_description
    if completed:
        project.is_completed = True
    else:
        project.is_completed = False
    project.created_by = request.user
    project.updated_by = request.user
    project.save()
    for user_obj in users:
        project.assign.add(user_obj[0])
    project.save()
    return redirect("view_projects", page_no=1)


@login_required
def edit_projects(request, project_id):
    if Project.objects.filter(
            Q(id=project_id) &
            Q(created_by=request.user)).exists():
        projects = Project.objects.get(id=project_id)
        users = User.objects.exclude(
            Q(username=request.user.username)
            | Q(is_active=False)
            | Q(is_superuser=True)
        )
        context = {"projects": projects, "users": users}
        return render(request, "project/edit_projects.html", context)
    else:
        messages.error(
            request, "You do not have permission to edit this project."
        )
        return redirect("view_projects", page_no=1)


@login_required
@require_POST
def update_projects(request):
    project_id = request.POST.get("project_id")
    assignee = request.POST.getlist("assignee")
    dead_line = request.POST.get("dead_line")
    description = request.POST.get("project_desc")
    completed = request.POST.get("completed")
    project = Project.objects.get(id=project_id)
    project.assign.clear()
    users = []
    for user in assignee:
        users.append(User.objects.filter(username=user))
    for user_obj in users:
        project.assign.add(user_obj[0])
    year, month, date = dead_line.split("-")
    _dead_line = datetime.date(int(year), int(month), int(date))
    project.dead_line = _dead_line
    project.description = description
    project.updated_by = request.user
    if completed:
        project.is_completed = True
    else:
        project.is_completed = False
    project.save()
    return redirect("view_projects", page_no=1)


@login_required
def search_projects(request):
    query = request.GET.get("query")
    page_no = request.GET.get("page_no")
    if page_no == "undefined":
        page_no = 1
    context = {}
    current_user = request.user
    projects = Project.objects.filter(
        Q(created_by=current_user) | Q(assign=current_user)
    ).values(
        "pk",
        "name",
        "acronym",
        "assign__username",
        "is_completed",
        "dead_line",
        "description",
        "tags",
        "created_by__username",
        "updated_by__username",
        "created_at",
        "updated_at",
    )
    if query is not None:
        projects = projects.filter(Q(name__icontains=query))
    paginator = Paginator(projects, 6)
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
