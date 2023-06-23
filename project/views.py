import datetime
import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from authentication.models import User
from project.models import Project, Task, CommonModel, Attachment,AuditHistory


# Create your views here.
@require_GET
@login_required
def view_projects(request, page_no):
    logging.info(
        f'[Request Method: {request.method}, '
        f'View Name: {__name__}, '
        f'User ID: {request.user.id}, '
        f'Data: {request.GET}, '
        f'URI: {request.build_absolute_uri()}]'
    )
    current_user = request.user
    my_projects = Project.objects.filter(
        (Q(created_by=current_user) | Q(assign=current_user))
        & Q(created_by__company=request.user.company)
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


@require_GET
@login_required
def add_projects(request):
    logging.info(
        f'[Request Method: {request.method}, '
        f'View Name: {__name__}, '
        f'User ID: {request.user.id}, '
        f'Data: {request.GET}, '
        f'URI: {request.build_absolute_uri()}]'
    )
    users = User.objects.filter(
        company=request.user.company
    ).exclude(
        Q(Q(username=request.user.username) | Q(is_superuser=True))
        & Q(is_active=False)
    )
    context = {"users": users}
    return render(request, "project/add_project.html", context)


@login_required
@require_POST
def insert_projects(request):
    logging.info(
        f'[Request Method: {request.method}, '
        f'View Name: {__name__}, '
        f'User ID: {request.user.id}, '
        f'Data: {request.POST}, '
        f'URI: {request.build_absolute_uri()}]'
    )
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


@require_GET
@login_required
def edit_projects(request, project_id):
    logging.info(
        f'[Request Method: {request.method}, '
        f'View Name: {__name__}, '
        f'User ID: {request.user.id}, '
        f'Data: {request.GET}, '
        f'URI: {request.build_absolute_uri()}]'
    )
    if Project.objects.filter(
            Q(id=project_id) &
            Q(created_by=request.user) &
            Q(created_by__company=request.user.company)
    ).exists():
        projects = Project.objects.get(id=project_id)
        users = User.objects.filter(
            company=request.user.company
        ).exclude(
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
    logging.info(
        f'[Request Method: {request.method}, '
        f'View Name: {__name__}, '
        f'User ID: {request.user.id}, '
        f'Data: {request.POST}, '
        f'URI: {request.build_absolute_uri()}]'
    )
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


@require_GET
@login_required
def search_projects(request):
    logging.info(
        f'[Request Method: {request.method}, '
        f'View Name: {__name__}, '
        f'User ID: {request.user.id}, '
        f'Data: {request.GET}, '
        f'URI: {request.build_absolute_uri()}]'
    )
    query = request.GET.get("query")
    page_no = request.GET.get("page_no")
    if page_no == "undefined":
        page_no = 1
    context = {}
    current_user = request.user
    projects = Project.objects.filter(
        Q(Q(created_by=current_user) | Q(assign=current_user))
        & Q(created_by__company=request.user.company)
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


# For Tasks.
@login_required()
def view_tasks(request, page_no=1):

    current_user = request.user
    my_tasks = Task.objects.filter((Q(assign=current_user) | Q(created_by=request.user)) & Q(is_deleted=False))
    projects = Project.objects.all()

    all_tasks = request.GET.get("task_filter")

    context = {}
    context["projects"] = projects

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
    users = User.objects.all().exclude(username="admin")
    projects = Project.objects.all()
    context = {'users': users, 'projects': projects}
    return render(request, 'task/add_task.html', context)


@login_required
@require_POST
def insert_tasks(request):
    task_name = request.POST.get('task_name')
    task_assignee = request.POST.get('assignee')
    task_description = request.POST.get('task_desc')
    task_related_project = request.POST.get('related-project-name')
    task_type = request.POST.get('task-type')
    task_status = request.POST.get('task-status')
    task_priority = request.POST.get('task-priority')
    project_acronym = Project.objects.get(pk=task_related_project)
    task_acronym_partial = project_acronym.acronym
    task_count = Task.objects.filter(project=task_related_project).exclude(is_deleted=True).count() + 1
    task_acronym_partial += "-" + str(task_count)
    task = Task()

    task.project = Project.objects.get(pk=task_related_project)
    task.assign = User.objects.get(pk=task_assignee)
    task.task_acronym = task_acronym_partial
    task.name = task_name
    task.description = task_description
    task.created_by = request.user
    task.updated_by = request.user
    task.task_priority = task_priority
    task.task_status = task_status
    task.task_type = task_type
    task.save()

    return redirect("view_tasks", page_no=1)


@login_required
def edit_tasks(request, task_id):
    if Task.objects.filter(Q(id=task_id) | Q(assign=request.user)).exists():
        tasks = Task.objects.get(id=task_id)
        users = User.objects.all().exclude(username="admin")
        projects = Project.objects.all()
        attachment_related_task = Task.objects.get(id=task_id)
        related_attachments = Attachment.objects.filter(task=attachment_related_task, is_deleted=False).distinct('document_name')
        activities = AuditHistory.objects.filter(project=tasks.project ,task = tasks).order_by('updated_at')

        context = {"tasks": tasks, "users": users, "projects": projects, "related_attachments": related_attachments, 'activities':activities}
        return render(request, "task/edit_tasks.html", context)
    else:
        return redirect("view_tasks", page_no=1)


@login_required
@require_POST
def update_tasks(request):
    task_id = request.POST.get("task_id")
    task_type = request.POST.get("task-type")
    assignee = request.POST.get("assignee")
    assignee_updated= request.POST.get("assignee-updated")
    user_object = User.objects.filter(Q(id=assignee) | Q(id=assignee_updated))[0]
    task_status = request.POST.get("task-status")
    task_priority = request.POST.get("task-priority")
    task_description = request.POST.get('description')
    task_attachments = list(set(request.FILES.getlist('upload[]')))
    attachment_related_task = Task.objects.get(id=task_id)
    old_documents = list(map(int, request.POST.getlist('old_documents')))
    saved_documents = list(Attachment.objects.filter(Q(task=task_id)&Q(is_deleted=False)).values_list('id',flat=True))

    for i in saved_documents:
        if i not in old_documents:

            delete = Attachment.objects.get(id=i)
            delete.is_deleted = True
            delete.save()
            audit_history = AuditHistory(
                task = attachment_related_task,
                project = attachment_related_task.project,
                action_by = request.user,
                action=f"Attachment " 
                       f"{delete.document_name} was deleted",
            )
            audit_history.save()



    for task_attachment in task_attachments:
        attachments = Attachment()
        attachments.document_name = task_attachment.name
        attachments.document = task_attachment
        attachments.task = attachment_related_task
        attachments.created_by = request.user
        attachments.updated_by = request.user
        attachments.save()

    print(task_attachments)
    task = Task.objects.filter(id=task_id).first()

    task.task_status = task_status
    task.task_priority = task_priority
    task.task_type = task_type
    task.description = task_description
    task.assign = user_object
    task.updated_by = request.user
    task.save()
    return redirect("edit_tasks", task_id=task_id)


@login_required
def search_tasks(request):
    query = request.GET.get('query')
    page_no = request.GET.get('page_no')
    print(page_no)
    if page_no == 'undefined':
        page_no = 1
    context = {}
    current_user = request.user
    tasks = Task.objects. \
        filter(Q(assign=current_user) & Q(is_deleted=False)).values('pk', 'name', 'task_acronym',
                                                                    'task_type',
                                                                    'project__name',
                                                                    'task_priority',
                                                                    'task_status',
                                                                    )
    if query is not None:
        tasks = tasks.filter(Q(name__icontains=query))

    paginator = Paginator(tasks, 10)
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
    print(context)
    print(tasks)
    return JsonResponse(context, safe=False)


@login_required
def filter_tasks(request):
    query = request.GET.get('query')
    page_no = request.GET.get('page_no')
    print(page_no)
    if page_no == 'undefined':
        page_no = 1
    context = {}
    current_user = request.user
    tasks = Task.objects. \
        filter(Q(assign=current_user) | Q(created_by=current_user)).exclude(is_deleted=True).values('pk', 'name',
                                                                                                    'task_acronym',
                                                                                                    'task_type',
                                                                                                    'project__name',
                                                                                                    'task_priority',
                                                                                                    'task_status',
                                                                                                    )
    if query is not None:
        tasks = tasks.filter(Q(project__name=query))

    paginator = Paginator(tasks, 10)
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
    print(context)
    print(tasks)
    return JsonResponse(context, safe=False)


@require_GET
@login_required
def view_project_tasks(request):
    logging.info(
        f'[Request Method: {request.method}, '
        f'View Name: {__name__}, '
        f'User ID: {request.user.id}, '
        f'Data: {request.GET}, '
        f'URI: {request.build_absolute_uri()}]'
    )
    project_id = request.GET.get('project_id')
    tasks = Task.objects.filter(
        Q(project=project_id) &
        Q(created_by__company=request.user.company) &
        (Q(created_by=request.user) | Q(updated_by=request.user))
    )
    assignee = tasks.distinct().values("assign_id", "assign__username")
    context = {'tasks': tasks, 'assign': assignee, 'project_id': project_id}
    return render(request, 'project/project_view_tasks.html', context)


@require_GET
@login_required
def project_filter_tasks(request):
    logging.info(
        f'[Request Method: {request.method}, '
        f'View Name: {__name__}, '
        f'User ID: {request.user.id}, '
        f'Data: {request.GET}, '
        f'URI: {request.build_absolute_uri()}]'
    )
    assign = request.GET.get('assign')
    priority = request.GET.get('priority')
    status = request.GET.get('status')
    project_id = request.GET.get('project_id')
    context = {}
    if project_id is not None:
        tasks = Task.objects.filter(
            Q(project=project_id) &
            Q(created_by__company=request.user.company) &
            (Q(created_by=request.user) | Q(updated_by=request.user))
        ).values(
            "pk",
            "task_acronym",
            "name",
            "assign__firstname",
            "assign__lastname",
            "task_priority",
            "task_status",
            "task_type"
            )
        if assign != 'null':
            tasks = tasks.filter(assign=assign)
        if priority != 'null':
            tasks = tasks.filter(task_priority=priority)
        if status != 'null':
            tasks = tasks.filter(task_status=status)
        context['tasks'] = list(tasks)
        return JsonResponse(context, safe=False)
    else:
        return redirect('view_projects')


@require_GET
@login_required
def project_search_tasks(request):
    logging.info(
        f'[Request Method: {request.method}, '
        f'View Name: {__name__}, '
        f'User ID: {request.user.id}, '
        f'Data: {request.GET}, '
        f'URI: {request.build_absolute_uri()}]'
    )
    query = request.GET.get('query')
    project_id = request.GET.get('project_id')
    context = {}
    if project_id is not None:
        tasks = Task.objects.filter(
            Q(project=project_id) &
            Q(created_by__company=request.user.company) &
            (Q(created_by=request.user) | Q(updated_by=request.user))
        ).values(
            "pk",
            "task_acronym",
            "name",
            "assign__firstname",
            "assign__lastname",
            "task_priority",
            "task_status",
            "task_type"
            )
        if query is not None:
            tasks = tasks.filter(name__icontains=query)
        context['tasks'] = list(tasks)
        return JsonResponse(context, safe=False)
    else:
        return redirect('view_projects')
