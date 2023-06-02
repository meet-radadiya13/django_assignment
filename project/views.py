import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from authentication.models import User
from project.encoder import LazyEncoder
from project.models import Project, Task


# Create your views here.
@login_required
def view_projects(request, page_no=1):
    current_user = request.user
    my_projects = Project.objects.filter(Q(created_by=current_user) | Q(assign=current_user))
    context = {}
    paginator = Paginator(my_projects, 6)
    page_obj = paginator.get_page(page_no)
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
    context["current_page"] = page_obj.number
    return render(request, 'project/project.html', context)


@login_required
def add_projects(request):
    users = User.objects.exclude(username=request.user.username)
    context = {'users': users}
    return render(request, 'project/add_project.html', context)


@login_required
@require_POST
def insert_projects(request):
    project_name = request.POST.get('project_name')
    project_acronym = request.POST.get('project_acronym')
    project_assignee = request.POST.getlist('assignee')
    dead_line = request.POST.get('dead_line')
    tags = request.POST.getlist('tags')
    project_description = request.POST.get('project_desc')
    completed = request.POST.get('completed')
    project = Project()
    users = []
    for user in project_assignee:
        users.append(User.objects.filter(username=user))
    project.name = project_name
    project.acronym = project_acronym
    year, month, date = dead_line.split('-')
    d = datetime.date(int(year), int(month), int(date))
    project.dead_line = d
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
    if Project.objects.filter(Q(id=project_id) & Q(created_by=request.user)).exists():
        projects = Project.objects.get(id=project_id)
        users = User.objects.exclude(Q(username=request.user.username) | Q(is_active=False))
        context = {'projects': projects, 'users': users}
        return render(request, 'project/edit_projects.html', context)
    else:
        messages.error(request, "You do not have permission to edit this project.")
        return redirect("view_projects", page_no=1)


@login_required
@require_POST
def update_projects(request):
    project_id = request.POST.get('project_id')
    assignee = request.POST.getlist('assignee')
    dead_line = request.POST.get('dead_line')
    description = request.POST.get('project_desc')
    completed = request.POST.get('completed')
    project = Project.objects.get(id=project_id)
    project.assign.clear()
    users = []
    for user in assignee:
        users.append(User.objects.filter(username=user))
    for user_obj in users:
        project.assign.add(user_obj[0])
    year, month, date = dead_line.split('-')
    d = datetime.date(int(year), int(month), int(date))
    project.dead_line = d
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
    query = request.GET.get('query')
    current_user = request.user
    projects = Project.objects.filter(Q(name__icontains=query) & (Q(created_by=current_user) | Q(assign=current_user)))
    data = serializers.serialize('json', projects, cls=LazyEncoder)
    return JsonResponse(data, safe=False)

#For Tasks.
@login_required()
def view_tasks(request, page_no=1):
    # current_user = request.user
    # my_tasks = Task.objects.filter(Q(assign=current_user))
    # context = {'my_tasks': my_tasks}
    # return render(request, 'task/task.html', context)

    current_user = request.user
    my_tasks = Task.objects.filter(Q(assign=current_user))
    projects= Project.objects.all()

    context = {}
    context["projects"] = projects

    if request.GET.get('task_filter'):
        featured_filter = request.GET.get('task_filter')
        listings = Task.objects.filter(project=featured_filter)
    else:
        listings = Task.objects.all()

    context["listings"] = listings




    paginator = Paginator(my_tasks, 10)
    page_obj = paginator.get_page(page_no)
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
    context["current_page"] = page_obj.number
    return render(request, 'task/task.html', context)


@login_required
def add_tasks(request):
    users = User.objects.all()
    projects = Project.objects.all()
    context = {'users': users, 'projects': projects}
    return render(request, 'task/add_task.html', context)


@login_required
@require_POST
def insert_tasks(request):
    task_name = request.POST.get('task_name')
    task_acronym = request.POST.get('task_acronym')
    task_assignee = request.POST.get('assignee')
    task_description = request.POST.get('task_desc')
    task_related_project = request.POST.get('related-project-name')
    task_type = request.POST['task-type']
    task_status = request.POST['task-status']
    task_priority = request.POST['task-priority']
    task = Task()

    task.project = Project.objects.get(pk=task_related_project)
    task.assign = User.objects.get(pk=task_assignee)
    task.name = task_name
    task.task_acronym = task_acronym
    task.description = task_description
    task.created_by = request.user
    task.updated_by = request.user
    task.task_priority = task_priority
    task.task_status = task_status
    task.task_type = task_type
    task.save()

    return redirect("view_tasks")

@login_required
def edit_tasks(request, task_id):
        pass


@login_required
@require_POST
def update_tasks(request):
        pass


# @login_required
# def task_filter(request):
#     projects = Project.objects.all()
#     context = {'projects': projects}
#     print(context)
#     return render(request, 'task/task.html', context)