from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name="home"),
    path('about/', views.About.as_view(), name='about'),
    path('projects/', views.ProjectList.as_view(), name='project_list'),
    path('projects/new/', views.ProjectCreate.as_view(), name="project_create"),
    path('projects/<int:pk>/', views.ProjectDetail.as_view(), name='project_detail'),
    path('projects/<int:pk>/update', views.ProjectUpdate.as_view(), name='project_update'),
    path('projects/<int:pk>/delete',views.ProjectDelete.as_view(), name='project_delete'),
    path('tasks/', views.TaskList.as_view(), name='task_list'),
    path('tasks/<int:pk>/complete', views.TaskComplete.as_view(), name='task_complete'),
    path('tasks/new/', views.TaskCreate.as_view(), name='task_create'),
    # add, detail, update and remove task from a project
    path('projects/<int:pk>/tasks/new/', views.TaskCreate.as_view(), name='project_task_create'),
    path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='task_detail'),
    path('tasks/<int:pk>/update', views.TaskUpdate.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete', views.TaskDelete.as_view(), name='task_delete'),

]
