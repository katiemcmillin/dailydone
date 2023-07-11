from django.db import models

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
    # collaborators = models.ManyToManyField(User, related_name='projects', blank=True)

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

    def __str__(self):
        return self.title