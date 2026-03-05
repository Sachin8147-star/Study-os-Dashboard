from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),

    # Theme
    path('api/theme/', views.set_theme, name='set_theme'),

    # Tasks
    path('api/tasks/', views.tasks_list, name='tasks_list'),
    path('api/tasks/create/', views.tasks_create, name='tasks_create'),
    path('api/tasks/<int:pk>/', views.task_detail, name='task_detail'),

    # Subjects
    path('api/subjects/', views.subjects_list, name='subjects_list'),
    path('api/subjects/create/', views.subjects_create, name='subjects_create'),

    # Notes
    path('api/notes/', views.notes_list, name='notes_list'),
    path('api/notes/save/', views.notes_save, name='notes_save'),

    # Habits
    path('api/habits/', views.habits_list, name='habits_list'),
    path('api/habits/create/', views.habits_create, name='habits_create'),
    path('api/habits/<int:pk>/toggle/', views.habit_toggle_day, name='habit_toggle_day'),
    path('api/habits/<int:pk>/delete/', views.habit_delete, name='habit_delete'),

    # Focus Sessions
    path('api/sessions/', views.sessions_list, name='sessions_list'),
    path('api/sessions/create/', views.sessions_create, name='sessions_create'),

    # Calendar Events
    path('api/events/', views.events_list, name='events_list'),
    path('api/events/create/', views.events_create, name='events_create'),
    path('api/events/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # Analytics
    path('api/analytics/', views.analytics, name='analytics'),
]
