from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]

    IMPORTANCE_CHOICES = [
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    ]

    title = models.CharField(max_length=400)
    description = models.TextField(max_length=4000)
    start_date = models.DateField()
    due_date = models.DateField()
    importance = models.CharField(max_length=100, choices=IMPORTANCE_CHOICES)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    contributors = models.ManyToManyField(User, related_name='contributed_projects', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Task(models.Model):
    IMPORTANCE_CHOICES = [
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    ]

    title = models.CharField(max_length=3000)
    description = models.TextField(max_length=4000, null=True)
    is_completed = models.BooleanField(default=False)
    importance = models.CharField(max_length=100, choices=IMPORTANCE_CHOICES)
    completion_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    contributors = models.ManyToManyField(User, related_name='contributed_tasks', blank=True)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check if in the save method if admin field is not provided when we save an new task. If the 2 condition are reunited we do the next step
        if not self.pk and not self.admin:
            self.admin = self._get_current_user()  # Set the admin field to the current user using Django's built-in authentication method _get_current_user
        super().save(*args, **kwargs)  # Call the original save method to save the task with the updated admin field

    def _get_current_user(self):
        return self.request.user  # Retrieve the currently logged-in user
    
class TaskComplete(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.task.title
    

