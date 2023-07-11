from django.urls import reverse
from django.shortcuts import redirect
from django.views import View 
from .models import Project, Task 
from django.http import HttpResponse 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView

from django.views.generic import DetailView

class Home(TemplateView):
    template_name = "home.html"

class About(TemplateView):
    template_name = "about.html"

# class Project :
#     def __init__(self, title, description, start_date, due_date, importance, status, created_at, updated_at):
#         self.title = title
#         self.idescription = description
#         self.start_date = start_date
#         self.due_date = due_date
#         self.importance = importance
#         self.status = status
#         self.created_at = created_at
#         self.updated_at = updated_at

# projects = [
#     Project(
#         "Productivity Tracker",
#         "Develop a productivity tracking application that helps users monitor and optimize their daily tasks. The app will include features such as task management, time tracking, goal setting, and performance analytics.",
#         "2022-01-01",
#         "2022-02-01",
#         "high",
#         "in_progress",
#         "2022-01-01 00:00:00",
#         "2022-01-01 00:00:00"
#     ),
#     Project(
#         "E-commerce Website Redesign",
#         "Redesign an existing e-commerce website to enhance the user experience, improve the visual aesthetics, and optimize the overall performance. The redesign will involve updating the UI/UX, implementing responsive design, and integrating new payment gateways.",
#         "2022-02-01",
#         "2022-03-01",
#         "medium",
#         "on_hold",
#         "2022-02-01 00:00:00",
#         "2022-02-01 00:00:00"
#     ),
#     Project(
#     "Website Content Migration",
#     "Migrate website content from an old platform to a new CMS...",
#     "2022-03-15",
#     "2022-04-15",
#     "high",
#     "in_progress",
#     "2022-03-01 00:00:00",
#     "2022-03-01 00:00:00"
# ),
# Project(
#     "Social Media Marketing Campaign",
#     "Plan and execute a social media marketing campaign...",
#     "2022-05-01",
#     "2022-06-30",
#     "medium",
#     "in_progress",
#     "2022-05-01 00:00:00",
#     "2022-05-01 00:00:00"
# ),
# Project(
#     "Mobile App UI/UX Design",
#     "Design user interfaces and experiences for a mobile application...",
#     "2022-07-01",
#     "2022-08-15",
#     "low",
#     "pending",
#     "2022-07-01 00:00:00",
#     "2022-07-01 00:00:00"
# ),
# Project(
#     "Data Migration and Integration",
#     "Migrate and integrate data from multiple sources into a unified system...",
#     "2022-09-01",
#     "2022-10-31",
#     "high",
#     "on_hold",
#     "2022-09-01 00:00:00",
#     "2022-09-01 00:00:00"
# ),
# ]

class ProjectCreate(CreateView):
    model = Project
    fields = ['title', 'description', 'start_date', 'due_date', 'importance', 'status']
    template_name = "project_create.html"

    # this will get the pk from the route and redirect to project view
    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})

class ProjectList(TemplateView):
    template_name = "project_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # to get the query parameter we have to acccess it in the request.GET dictionary object        
        title = self.request.GET.get("title")
        # If a query exists we will filter by title 
        if title != None:
            # .filter is the sql WHERE statement and title__icontains is doing a search for any title that contains the query param
            context["projects"] = Project.objects.filter(title__icontains=title)
            # We add a header context that includes the search param
            context["header"] = f"Searching for {title}"
        else:
            context["projects"] = Project.objects.all()
            # default header for not searching 
            context["header"] = "List Of Projects"
        return context
    

class ProjectDetail(DetailView):
    model = Project
    template_name = "project_detail.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     project_id = kwargs['project_id']
    #     # Retrieve the project object based on the project_id
    #     # Add the project object to the context
    #     return context

class ProjectUpdate(UpdateView):
    model = Project
    fields = ['title', 'description', 'start_date', 'due_date', 'importance', 'status']
    template_name = "project_update.html"

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})
    
class ProjectDelete(DeleteView):
    model = Project
    template_name = "project_delete_confirmation.html"
    success_url = "/projects/"

class TaskCreate(View):

    def post(self, request, pk):
        title = request.POST.get("title")
        description = request.POST.get("description")
        is_completed = request.POST.get("is_completed")
        importance = request.POST.get("importance")
        completion_date = request.POST.get("completion_date")
        due_date = request.POST.get("due_date")
        created_at = request.POST.get("create_at")

        project = Project.objects.get(pk=pk)
        Task.objects.create(
            title=title,
            description=description,
            is_completed=is_completed,
            importance=importance,
            completion_date=completion_date,
            due_date=due_date,
            created_at=created_at,
            project=project
        )
        return redirect('project_detail', pk=pk)
    