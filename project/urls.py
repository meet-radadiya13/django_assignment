from django.urls import path

from project import views

urlpatterns = [
    path(
        "view_projects/<page_no>/", views.view_projects, name="view_projects"
    ),
    path("add_projects/", views.add_projects, name="add_projects"),
    path("insert_projects/", views.insert_projects, name="insert_projects"),
    path(
        "edit_projects/<int:project_id>/",
        views.edit_projects,
        name="edit_projects",
    ),
    path("update_projects/", views.update_projects, name="update_projects"),
    path("search_projects/", views.search_projects, name="search_projects"),

    path("view_tasks/<int:page_no>", views.view_tasks, name="view_tasks"),
    path("add_tasks/", views.add_tasks, name="add_tasks"),
    path("insert_tasks/", views.insert_tasks, name="insert_tasks"),
    path("edit_tasks/<int:task_id>/", views.edit_tasks, name="edit_tasks"),
    path("update_tasks/", views.update_tasks, name="update_tasks"),
    path("search_tasks/", views.search_tasks, name="search_tasks"),
    path("filter_tasks/", views.filter_tasks, name="filter_tasks"),

]
