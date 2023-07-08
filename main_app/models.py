from django.db import models

# Create your models here.

class Project(models.Model):
    IMPORTANCE_CHOICES = [
        ('high', 'High Priority'),
        ('medium', 'Medium Priority'),
        ('low', 'Low Priority'),
    ]

    title = models.CharField(max_length=400)
    description = models.TextField(max_length=4000)
    start_date = models.DateField()
    end_date = models.DateField()
    importance = models.CharField(max_length=100, choices=IMPORTANCE_CHOICES)
    # collaborators = models.ManyToManyField(User, related_name='projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
