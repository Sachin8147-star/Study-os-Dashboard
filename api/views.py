import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from .models import (
    UserProfile, Task, Subject, Note, Habit,
    HabitDay, FocusSession, CalendarEvent
)


def get_or_create_profile(user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    return profile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if not username or not password:
            error = 'Username and password are required.'
        elif password != password2:
            error = 'Passwords do not match.'
        elif User.objects.filter(username=username).exists():
            error = 'Username already taken.'
        else:
            user = User.objects.create_user(username=username, password=password)
            get_or_create_profile(user)
            # Seed default subjects
            colors = ['#7c6aff','#ff6a9b','#6affd4','#ffd96a']
            defaults = ['Mathematics','Physics','Chemistry','English']
            for i, name in enumerate(defaults):
                Subject.objects.create(user=user, name=name, color=colors[i])
            login(request, user)
            return redirect('/')
    return render(request, 'api/register.html', {'error': error})


@login_required
def index(request):
    profile = get_or_create_profile(request.user)
    return render(request, 'api/index.html', {'theme': profile.theme, 'username': request.user.username})


# =========== THEME ===========
@login_required
@require_http_methods(['POST'])
def set_theme(request):
    data = json.loads(request.body)
    theme = data.get('theme', 'dark')
    profile = get_or_create_profile(request.user)
    profile.theme = theme
    profile.save()
    return JsonResponse({'ok': True, 'theme': theme})


# =========== TASKS ===========
@login_required
def tasks_list(request):
    tasks = Task.objects.filter(user=request.user)
    return JsonResponse({'tasks': [t.to_dict() for t in tasks]})


@login_required
@require_http_methods(['POST'])
def tasks_create(request):
    data = json.loads(request.body)
    task = Task.objects.create(
        user=request.user,
        text=data.get('text', ''),
        priority=data.get('priority', 'med'),
        subject=data.get('subject', ''),
    )
    return JsonResponse({'task': task.to_dict()}, status=201)


@login_required
@require_http_methods(['PATCH', 'DELETE'])
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'DELETE':
        task.delete()
        return JsonResponse({'ok': True})
    data = json.loads(request.body)
    if 'done' in data:
        task.done = data['done']
    if 'text' in data:
        task.text = data['text']
    if 'priority' in data:
        task.priority = data['priority']
    task.save()
    return JsonResponse({'task': task.to_dict()})


# =========== SUBJECTS ===========
@login_required
def subjects_list(request):
    subjects = Subject.objects.filter(user=request.user)
    return JsonResponse({'subjects': [s.to_dict() for s in subjects]})


@login_required
@require_http_methods(['POST'])
def subjects_create(request):
    data = json.loads(request.body)
    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name required'}, status=400)
    colors = ['#7c6aff','#ff6a9b','#6affd4','#ffd96a','#ff9f2f','#6aaff6','#f06aff','#6affb0']
    count = Subject.objects.filter(user=request.user).count()
    color = data.get('color', colors[count % len(colors)])
    subj, created = Subject.objects.get_or_create(user=request.user, name=name, defaults={'color': color})
    return JsonResponse({'subject': subj.to_dict()}, status=201 if created else 200)


# =========== NOTES ===========
@login_required
def notes_list(request):
    notes = Note.objects.filter(user=request.user).select_related('subject')
    return JsonResponse({'notes': [n.to_dict() for n in notes]})


@login_required
@require_http_methods(['POST'])
def notes_save(request):
    data = json.loads(request.body)
    subject_id = data.get('subject_id')
    subj = get_object_or_404(Subject, pk=subject_id, user=request.user)
    note, _ = Note.objects.get_or_create(user=request.user, subject=subj)
    note.title = data.get('title', '')
    note.content = data.get('content', '')
    note.save()
    return JsonResponse({'note': note.to_dict()})


# =========== HABITS ===========
@login_required
def habits_list(request):
    habits = Habit.objects.filter(user=request.user).prefetch_related('habit_days')
    return JsonResponse({'habits': [h.to_dict() for h in habits]})


@login_required
@require_http_methods(['POST'])
def habits_create(request):
    data = json.loads(request.body)
    habit = Habit.objects.create(
        user=request.user,
        name=data.get('name', ''),
        icon=data.get('icon', '✦'),
    )
    for i in range(7):
        HabitDay.objects.create(habit=habit, day_index=i, done=False)
    return JsonResponse({'habit': habit.to_dict()}, status=201)


@login_required
@require_http_methods(['PATCH'])
def habit_toggle_day(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    data = json.loads(request.body)
    day_idx = data.get('day_index')
    hd, _ = HabitDay.objects.get_or_create(habit=habit, day_index=day_idx)
    hd.done = not hd.done
    hd.save()
    habit.streak = HabitDay.objects.filter(habit=habit, done=True).count()
    habit.save()
    return JsonResponse({'habit': habit.to_dict()})


@login_required
@require_http_methods(['DELETE'])
def habit_delete(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    habit.delete()
    return JsonResponse({'ok': True})


# =========== FOCUS SESSIONS ===========
@login_required
def sessions_list(request):
    sessions = FocusSession.objects.filter(user=request.user)[:50]
    total_mins = sum(s.duration for s in FocusSession.objects.filter(user=request.user))
    return JsonResponse({
        'sessions': [s.to_dict() for s in sessions],
        'total_sessions': FocusSession.objects.filter(user=request.user).count(),
        'total_mins': total_mins,
    })


@login_required
@require_http_methods(['POST'])
def sessions_create(request):
    data = json.loads(request.body)
    session = FocusSession.objects.create(
        user=request.user,
        subject=data.get('subject', 'General'),
        duration=data.get('duration', 25),
    )
    # Update streak
    profile = get_or_create_profile(request.user)
    profile.streak_count += 1
    profile.save()
    return JsonResponse({'session': session.to_dict()}, status=201)


# =========== CALENDAR EVENTS ===========
@login_required
def events_list(request):
    events = CalendarEvent.objects.filter(user=request.user)
    return JsonResponse({'events': [e.to_dict() for e in events]})


@login_required
@require_http_methods(['POST'])
def events_create(request):
    data = json.loads(request.body)
    event = CalendarEvent.objects.create(
        user=request.user,
        name=data.get('name', ''),
        date=data.get('date'),
        time=data.get('time') or None,
        color=data.get('color', '#7c6aff'),
    )
    return JsonResponse({'event': event.to_dict()}, status=201)


@login_required
@require_http_methods(['DELETE'])
def event_delete(request, pk):
    event = get_object_or_404(CalendarEvent, pk=pk, user=request.user)
    event.delete()
    return JsonResponse({'ok': True})


# =========== ANALYTICS ===========
@login_required
def analytics(request):
    from django.utils import timezone
    from datetime import timedelta
    import datetime
    today = timezone.now().date()
    days = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        count = FocusSession.objects.filter(user=request.user, created_at__date=d).count()
        mins = sum(
            s.duration for s in FocusSession.objects.filter(user=request.user, created_at__date=d)
        )
        tasks_done = Task.objects.filter(user=request.user, done=True, updated_at__date=d).count()
        days.append({
            'label': d.strftime('%a'),
            'date': d.isoformat(),
            'sessions': count,
            'minutes': mins,
            'tasks_done': tasks_done,
        })
    profile = get_or_create_profile(request.user)
    return JsonResponse({
        'days': days,
        'streak': profile.streak_count,
        'total_sessions': FocusSession.objects.filter(user=request.user).count(),
        'total_tasks': Task.objects.filter(user=request.user, done=True).count(),
    })
    return "/register_view/"
