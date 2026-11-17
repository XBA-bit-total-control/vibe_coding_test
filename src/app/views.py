from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import translation
from django.views.decorators.http import require_http_methods, require_safe
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer


TASK_DATE_ORDERING = {
    "new": ("-created_at", "-pk"),
    "old": ("created_at", "pk"),
}


def _filtered_tasks(owner, status, date_order):
    queryset = Task.objects.filter(owner=owner)
    if status is not None:
        queryset = queryset.filter(status=status)
    return queryset.order_by(*TASK_DATE_ORDERING[date_order])


@login_required(login_url="login")
@require_safe
def task_list(request):
    status = request.GET.get("status")
    if status not in dict(Task.STATUS_CHOICES):
        status = None

    date_order = request.GET.get("date", "new")
    if date_order not in TASK_DATE_ORDERING:
        date_order = "new"

    return render(request, "app/tasks.html", {
        "tasks": _filtered_tasks(request.user, status, date_order),
        "statuses": Task.STATUS_CHOICES,
        "selected_status": status,
        "date_order": date_order,
    })


@login_required(login_url="login")
@require_safe
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    return render(request, "app/task_detail.html", {"task": task, "statuses": Task.STATUS_CHOICES})


@api_view(["GET", "POST"])
def tasks(request):
    if request.method == "GET":
        status = request.query_params.get("status")
        date_order = request.query_params.get("date", "new")

        if status is not None and status not in dict(Task.STATUS_CHOICES):
            return Response({"error": "Некорректный статус"}, status=400)

        if date_order not in TASK_DATE_ORDERING:
            return Response({"error": "Некорректный порядок сортировки"}, status=400)

        queryset = _filtered_tasks(request.user, status, date_order)

        return Response(TaskSerializer(queryset, many=True).data)

    if request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)

        return Response(serializer.data, status=201)


@api_view(["GET", "PATCH", "DELETE"])
def task_by_id(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if task.owner.id != request.user.id:
        return Response(
            {"error": "Вы не являетесь владельцем задачи"},
            status=403
        )

    if request.method == "GET":
        serializer = TaskSerializer(task)

        return Response(serializer.data)

    if request.method == "PATCH":
        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    if request.method == "DELETE":
        task.delete()

        return Response(status=204)


@require_http_methods(["GET", "POST"])
def register(request):
    with translation.override("ru"):
        form = UserCreationForm(request.POST if request.method == "POST" else None)
        form.fields["password1"].help_text = ""
        form.fields["password2"].help_text = ""
        if request.method == "POST" and form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task_list")

        return render(request, "registration/register.html", {"form": form})
