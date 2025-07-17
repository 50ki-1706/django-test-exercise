from django.shortcuts import render, redirect
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from todo.models import Task
import django.http
from django.http import Http404


# Create your views here.
def index(request: django.http.HttpRequest) -> django.http.HttpResponse:
    if request.method == "POST":
        due: timezone.datetime | None = parse_datetime(request.POST.get("due_at", ""))
        task: Task = Task(
            title=request.POST["title"],
            due_at=make_aware(due) if due else None,
        )
        task.save()

    if request.GET.get("order") == "due":
        tasks: list[Task] = Task.objects.filter(completed=False).order_by("due_at")
    else:
        tasks: list[Task] = Task.objects.filter(completed=False).order_by("-posted_at")
    context: dict[str, list[Task]] = {"tasks": tasks}
    return render(request, "todo/index.html", context)


def detail(request: django.http.HttpRequest, task_id: int) -> django.http.HttpResponse:
    try:
        task: Task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    context: dict[str, Task] = {"task": task}
    return render(request, "todo/detail.html", context)


def update(request: django.http.HttpRequest, task_id: int) -> django.http.HttpResponse:
    try:
        task: Task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == "POST":
        task.title = request.POST["title"]
        task.due_at = make_aware(parse_datetime(request.POST["due_at"]))
        task.save()
        return redirect(detail, task_id)
    context: dict[str, Task] = {"task": task}
    return render(request, "todo/edit.html", context)


def delete(request: django.http.HttpRequest, task_id: int) -> django.http.HttpResponse:
    try:
        task: Task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect(index)


def close(request, task_id) -> django.http.HttpResponse:
    try:
        task: Task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(completed_tasks)


def completed_tasks(request: django.http.HttpRequest) -> django.http.HttpResponse:
    tasks: list[Task] = Task.objects.filter(completed=True).order_by("-posted_at")
    context: dict[str, list[Task]] = {"completed_tasks": tasks}
    return render(request, "todo/completed.html", context)
