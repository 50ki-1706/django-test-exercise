from django.shortcuts import render
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task
import django.http
import django


# Create your views here.
def index(request: django.http.HttpRequest) -> django.http.HttpResponse:
    if request.method == "POST":
        due = parse_datetime(request.POST.get("due_at", ""))
        task = Task(
            title=request.POST["title"],
            due_at=make_aware(due) if due else None,
        )
        task.save()

    if request.GET.get("order") == "due":
        tasks = Task.objects.order_by("due_at")
    else:
        tasks = Task.objects.order_by("-created_at")
    context = {"tasks": tasks}
    return render(request, "todo/index.html", context)
