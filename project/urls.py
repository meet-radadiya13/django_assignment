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
    path("view_project_tasks/", views.view_project_tasks,
         name="view_project_tasks"),
    path("project_filter_tasks/", views.project_filter_tasks,
         name="project_filter_tasks"),
    path("project_search_tasks/", views.project_search_tasks,
         name="project_search_tasks"),
]
