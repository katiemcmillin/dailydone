from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Project, Task, TaskComplete, UserProfile
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.views.generic import DetailView, ListView
from django.db.models import Q
from datetime import date, datetime
from django.forms import ModelForm



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
            # .filter is the sql WHERE statement and title__icontains is doing a search for any title that contains the query param and link to the admin who is links to the project and keep only the project that are NOT completed
            context["projects"] = Project.objects.filter(title__icontains=title, admin=self.request.user, is_completed=False)
            # We add a header context that includes the search param
            context["header"] = f"Searching for {title}"
        else:
            context["projects"] = Project.objects.filter(admin=self.request.user, is_completed=False)
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
    fields = ['title', 'description', 'start_date', 'due_date', 'importance', 'status', 'admin', 'contributors', 'is_completed']
    template_name = "project_update.html"

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.pk})


@method_decorator(login_required, name='dispatch')
class ProjectDelete(DeleteView):
    model = Project
    template_name = "project_delete_confirmation.html"
    success_url = "/projects/"

# handle the action of marking a project as completed
@method_decorator(login_required, name='dispatch')
class ProjectComplete(View):
    def post(self, request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'], admin=request.user)
        project.is_completed = True
        project.save()
        return redirect('project_list')

# CompletedProjectList is intended to handle a GET request and display the list of completed projects   
@method_decorator(login_required, name='dispatch')
class CompletedProjectList(TemplateView):
    template_name = "completed_project_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["completed_projects"] = Project.objects.filter(is_completed=True, admin=self.request.user)
        return context


@method_decorator(login_required, name='dispatch')
class TaskList(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'
    ordering = 'due_date'

    # to see task that are not completed yet 'is_completed=False'
    def get_queryset(self):
        return Task.objects.filter(Q(admin=self.request.user) | Q(contributors=self.request.user), is_completed=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_tasks'] = Task.objects.filter(Q(admin=self.request.user) | Q(contributors=self.request.user), is_completed=True)
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
    
    def post(self, request, *args, **kwargs):
        task = get_object_or_404(Task, pk=kwargs['pk'])
        if 'is_completed' in request.POST:
            task.is_completed = True
            task.save()
        return redirect('task_list')


@method_decorator(login_required, name='dispatch')
class TaskCompletedList(ListView):
    model = Task
    template_name = 'task_completed_list.html'
    context_object_name = 'tasks'  

    # Utilisation of Q objects that allow for complex lookups in Django. Here we check if the logged-in user is either the admin or a contributor with Q object filters filtering tasks that are set as completed. the filter conditions are separated by pipe '|'
    def get_queryset(self):
        return Task.objects.filter(Q(admin=self.request.user) | Q(contributors=self.request.user), is_completed=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['completed_tasks'] = self.get_queryset()
        return context

@method_decorator(login_required, name='dispatch')
class TaskCompleteView(View):
    template_name = "task_complete.html"

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed  

        task.save()
        return redirect('task_list')


# This view is for creating a Task with multiple associated projects
@method_decorator(login_required, name='dispatch')
class TaskCreateWithProjects(CreateView):
    model = Task
    fields = ['title', 'description', 'is_completed', 'importance','project', 'due_date', 'contributors']
    template_name = 'task_create.html'
    success_url = "/tasks/" 

# access to all the projects to pick in the list
    def get_context_data(self, **kwargs):
        context = super().get_context_data( **kwargs)
        context['projects'] = Project.objects.all()
        return context
    
    def form_valid(self, form):
        task = form.save(commit=False)
        task.admin = self.request.user  # assign the current user as admin automatically
        task.save()
        form.save_m2m()  # necessary to save MToM relationship
        return redirect(self.success_url)


# This view is for creating a Task within a specific project
@method_decorator(login_required, name='dispatch')
class TaskCreateWithProject(CreateView):
    model = Task
    template_name = 'task_create.html'
    fields = ['title', 'description', 'is_completed', 'importance', 'due_date', 'contributors']
    
    def form_valid(self, form):
        form.instance.admin = self.request.user  # Set the current user as the admin of the task
        form.instance.project = get_object_or_404(Project, pk=self.kwargs['pk'])  # set the project
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project_detail', kwargs={'pk': self.object.project.pk}) 



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
    


@method_decorator(login_required, name='dispatch')
class UserProfileView(DetailView):
    model = User
    template_name = 'registration/user_profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        user = self.request.user
        UserProfile.objects.get_or_create(user=user) # this will create UserProfile if it doesn't exist
        return user
        
        

#  To create a form 
class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'location', 'interests', 'picture']


# Use the form here 
@method_decorator(login_required, name='dispatch')        
class UserProfileViewUpdate(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'registration/user_profile_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_profile'] = self.request.user.userprofile
        return context

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_success_url(self):
        return reverse('user_profile', kwargs={'pk': self.request.user.pk})

    

@method_decorator(login_required, name='dispatch')
class Dashboard(View):
    template_name = 'dashboard.html'

    def get(self, request):
        # Fetching all tasks and projects where the logged-in user is the admin and or collaborator
        tasks = Task.objects.filter(Q(admin=request.user) | Q(contributors=request.user))
        projects = Project.objects.filter(Q(admin=request.user) | Q(contributors=request.user))

        # Fetching tasks due today
        tasks_today = tasks.filter(due_date=date.today())
        
        # Fetching upcoming tasks
        tasks_upcoming = tasks.filter(due_date__gt=date.today())

        # Fetching the projects due today
        projects_today = projects.filter(due_date=date.today())

        # Fetching remaining tasks and projects
        tasks_remaining = tasks.filter(is_completed=False)
        projects_remaining = projects.filter(is_completed=False)

        context = {
            'tasks_today': tasks_today,
            'tasks_upcoming': tasks_upcoming,
            'projects_today': projects_today,
            'tasks_remaining': tasks_remaining,
            'projects_remaining': projects_remaining,
            'current_date': datetime.now(), 
        }
        
        return render(request, self.template_name, context)
