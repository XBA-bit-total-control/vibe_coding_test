from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "status", "owner", "created_at")
        read_only_fields = ("id", "owner", "created_at")

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Название задачи должно быть не короче 5 символов")
        return value

    def validate_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Описание задачи должно быть не короче 10 символов")
        return value
