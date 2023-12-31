# Generated by Django 4.2.2 on 2023-07-11 04:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='end_date',
            new_name='due_date',
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=3000)),
                ('description', models.TextField(max_length=4000)),
                ('is_completed', models.BooleanField(default=False)),
                ('importance', models.CharField(choices=[('high', 'High Priority'), ('medium', 'Medium Priority'), ('low', 'Low Priority')], max_length=100)),
                ('completion_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='main_app.project')),
            ],
        ),
    ]
