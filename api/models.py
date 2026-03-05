from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    theme = models.CharField(max_length=10, default='dark', choices=[('dark','Dark'),('light','Light')])
    streak_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Task(models.Model):
    PRIORITY_CHOICES = [('high','High'),('med','Medium'),('low','Low')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    text = models.CharField(max_length=500)
    done = models.BooleanField(default=False)
    priority = models.CharField(max_length=4, choices=PRIORITY_CHOICES, default='med')
    subject = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.text

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'done': self.done,
            'priority': self.priority,
            'subject': self.subject,
            'created_at': self.created_at.isoformat(),
        }


class Subject(models.Model):
    COLORS = ['#7c6aff','#ff6a9b','#6affd4','#ffd96a','#ff9f2f','#6aaff6','#f06aff','#6affb0']
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20, default='#7c6aff')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        unique_together = ['user', 'name']

    def __str__(self):
        return self.name

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'color': self.color}


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=300, blank=True)
    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subject.name}: {self.title}"

    def to_dict(self):
        return {
            'id': self.id,
            'subject_id': self.subject.id,
            'title': self.title,
            'content': self.content,
            'updated_at': self.updated_at.isoformat(),
        }


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=10, default='✦')
    streak = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def to_dict(self):
        days = list(self.habit_days.order_by('day_index').values_list('done', flat=True))
        while len(days) < 7:
            days.append(False)
        return {
            'id': self.id,
            'name': self.name,
            'icon': self.icon,
            'streak': self.streak,
            'days': days[:7],
        }


class HabitDay(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='habit_days')
    day_index = models.IntegerField()  # 0-6 Mon-Sun
    done = models.BooleanField(default=False)

    class Meta:
        unique_together = ['habit', 'day_index']


class FocusSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='focus_sessions')
    subject = models.CharField(max_length=100, default='General')
    duration = models.IntegerField(default=25)  # minutes
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.subject} ({self.duration}m)"

    def to_dict(self):
        return {
            'id': self.id,
            'subject': self.subject,
            'duration': self.duration,
            'time': self.created_at.strftime('%I:%M %p'),
            'created_at': self.created_at.isoformat(),
        }


class CalendarEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    name = models.CharField(max_length=300)
    date = models.DateField()
    time = models.TimeField(null=True, blank=True)
    color = models.CharField(max_length=50, default='#7c6aff')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date,
            'time': self.time.strftime('%H:%M') if self.time else '',
            'color': self.color,
        }
