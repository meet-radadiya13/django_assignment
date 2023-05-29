import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from authentication.models import User
from project.models import Project


# Create your views here.
@login_required
def view_projects(request):
    current_user = request.user
    my_projects = Project.objects.filter(Q(created_by=current_user) | Q(assign=current_user))
    context = {'my_projects': my_projects}
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
        users.append(User.objects.filter(email=user))
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

    for i in users:
        project.assign.add(i[0])

    project.save()

    return redirect("view_projects")


@login_required
def edit_projects(request, project_id):
    projects = Project.objects.get(id=project_id)
    users = User.objects.exclude(username=request.user.username)
    context = {'projects': projects, 'users': users}
    return render(request, 'project/edit_projects.html', context)


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
        users.append(User.objects.filter(email=user))
    for i in users:
        project.assign.add(i[0])

    year, month, date = dead_line.split('-')
    d = datetime.date(int(year), int(month), int(date))
    project.dead_line = d

    project.description = description

    if completed:
        project.is_completed = True
    else:
        project.is_completed = False

    project.save()

    return redirect("view_projects")
