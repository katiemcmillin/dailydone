from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Project, Task, TaskComplete, UserProfile
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView


class PublicHome(TemplateView):
    template_name = "public_home.html"

@method_decorator(login_required, name='dispatch')
class PrivateHome(TemplateView):
    template_name = "private_home.html"

class Signup(View):
    # show a form to fill out
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    # on form submit, validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("project_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)



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

@method_decorator(login_required, name='dispatch')
class ProjectCreate(CreateView):
    model = Project
    fields = ['title', 'description', 'start_date', 'due_date', 'importance', 'status', 'admin', 'contributors']
    template_name = "project_create.html"

    def form_valid(self, form):
        form.instance.admin = self.request.user  # logged-in admin(user) to the form
        self.object = form.save()  # I store the newly created Project instance to access its 'pk'
        return redirect('project_task_create', self.object.pk)  # I redirect to the 'project_task_create' view, passing the newly created Project's 'pk'

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class ProjectList(TemplateView):
    template_name = "project_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # to get the query parameter we have to acccess it in the request.GET dictionary object        
        title = self.request.GET.get("title")
        # If a query exists we will filter by title 
        if title != None:
            # .filter is the sql WHERE statement and title__icontains is doing a search for any title that contains the query param and link to the admin who is links to the project
            context["projects"] = Project.objects.filter(title__icontains=title, admin=self.request.user)
            # We add a header context that includes the search param
            context["header"] = f"Searching for {title}"
        else:
            context["projects"] = Project.objects.filter(admin=self.request.user)
            # default header for not searching 
            context["header"] = "List Of Projects"
        return context

@method_decorator(login_required, name='dispatch')
class ProjectDetail(DetailView):
    model = Project  
    template_name = "project_detail.html"  

    # Override the get_context_data method
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  
        context['tasks'] = Task.objects.filter(project=self.object, is_completed=False)
        return context

    def post(self, request, *args, **kwargs):
        project = self.get_object()  # Get the Project instance
        task_ids = request.POST.getlist('task_ids[]')  # Get the task IDs from the request POST data
        # Filter tasks that have an ID in task_ids
        print(task_ids) 
        completed_tasks = Task.objects.filter(pk__in=task_ids)
        
        for task in completed_tasks:
            task.is_completed = True  # Mark the task as completed
            task.save()  # Save the changes
            TaskComplete.objects.create(task=task)  # Create a TaskComplete instance for the task
        
        return redirect('project_detail', pk=project.pk)

@method_decorator(login_required, name='dispatch')
class ProjectUpdate(UpdateView):
    model = Project
    fields = ['title', 'description', 'start_date', 'due_date', 'importance', 'status', 'admin', 'contributors']
    template_name = "project_update.html"

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class ProjectDelete(DeleteView):
    model = Project
    template_name = "project_delete_confirmation.html"
    success_url = "/projects/"

@method_decorator(login_required, name='dispatch')
class TaskCreate(View):
    def post(self, request, pk):
        title = request.POST.get("title")
        description = request.POST.get("description")
        # look if is_completed's box is checked. if yes, the value will be True otherwise it will be false
        is_completed = request.POST.get("is_completed") == "on"  
        importance = request.POST.get("importance")
        completion_date = request.POST.get("completion_date")
        due_date = request.POST.get("due_date")
        created_at = request.POST.get("create_at")
        admin = request.POST.get("admin")
        contributors = request.POST.get("contributors")

        project = Project.objects.get(pk=pk)
        admin = request.user  # Get the current user as the admin (user) of the task
        Task.objects.create(
            title=title,
            description=description,
            is_completed=is_completed,
            importance=importance,
            completion_date=completion_date,
            due_date=due_date,
            created_at=created_at,
            project=project,
            admin=admin,    # Assign the admin (user) to the task
            contributors=contributors
        )
        return redirect('project_detail', pk=pk)

@method_decorator(login_required, name='dispatch')
class TaskList(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    ordering = 'due_date'

    def get_queryset(self):
        # Filter tasks based on the logged-in user as the admin
        return Task.objects.filter(admin=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_tasks'] = Task.objects.filter(is_completed=True)
        return context
    
@method_decorator(login_required, name='dispatch')
class TaskDetail(DetailView):
    model = Task
    template_name = 'task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object  

        context['admin'] = task.admin.username
        context['contributors'] = ", ".join([contributor.username for contributor in task.contributors.all()])
        return context

@method_decorator(login_required, name='dispatch')
class TaskCompletedList(ListView):
    model = Task
    template_name = 'task_completed_list.html'
    context_object_name = 'tasks'  

    def get_queryset(self):
        return Task.objects.filter(is_completed=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_tasks'] = self.get_queryset()
        return context

@method_decorator(login_required, name='dispatch')
class TaskComplete(TemplateView):
    template_name = "task_complete.html"

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        TaskComplete.objects.create(task=task)
        return redirect('task_list')
    
    def task_complete(request):
        completed_tasks = Task.objects.filter(is_completed=True)
        context = {'completed_tasks': completed_tasks}

        return render(request, 'task_complete.html', context)

@method_decorator(login_required, name='dispatch')
class TaskCreate(CreateView):
    model = Task
    fields = ['title', 'description', 'is_completed', 'importance','project', 'due_date', 'admin', 'contributors']
    template_name = 'task_create.html'
    success_url = "/tasks/" 

# access to all the projects to pick in the list
    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context['projects'] = Project.objects.all()
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            task = form.save()  # save the new task instance
            projects = request.POST.getlist('projects')  # I get the list of selected project ids
            for project_id in projects:
                project = Project.objects.get(pk=project_id)
                task.projects.add(project)  # I add each selected project to the task
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

@method_decorator(login_required, name='dispatch')       
class TaskUpdate(UpdateView):
    model = Task
    template_name = 'task_update.html'
    fields = ['title', 'description', 'is_completed', 'importance', 'project', 'due_date', 'admin', 'contributors']

    def get_success_url(self):
        return reverse('task_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class TaskDelete(DeleteView):
    model = Task
    template_name = "task_delete_confirmation.html"

    def get_success_url(self):
        return reverse('task_list')  # redirect to task_list after deleting a task

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        return response


class UserProfileView(DetailView):
    model = UserProfile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = UserProfile.objects.all() 
        context = super(UserProfileView, self).get_context_data(*args, **kwargs)
        # Grabe the user Page from the database and  retrieve the user profile associated with the logged-in user
        user_pg = get_object_or_404(UserProfile, pk=self.request.user.pk)
        context["user_profile"] = user_pg
        return context
