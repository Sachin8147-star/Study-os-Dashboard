from django.contrib import admin
from .models import UserProfile, Task, Subject, Note, Habit, HabitDay, FocusSession, CalendarEvent

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'theme', 'streak_count']

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'done', 'priority', 'subject', 'created_at']
    list_filter = ['done', 'priority']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'color']

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'title', 'updated_at']

@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'icon', 'streak']

@admin.register(FocusSession)
class FocusSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'duration', 'created_at']

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'date', 'time']
