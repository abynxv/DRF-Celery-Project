from rest_framework import serializers
from .models import TaskResult, EmailTask


class TaskResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskResult
        fields = '__all__'

class EmailTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailTask
        fields = '__all__'
        read_only_fields = ('task_id', 'is_sent', 'created_at')

class LongRunningTaskSerializer(serializers.Serializer):
    duration = serializers.IntegerField(min_value=1, max_value=60, default=10)

class AddNumbersSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()

class MultiplyNumbersSerializer(serializers.Serializer):
    x = serializers.IntegerField()
    y = serializers.IntegerField()

class ProcessDataSerializer(serializers.Serializer):
    data = serializers.ListField(child=serializers.CharField())

class TaskStatusSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    status = serializers.CharField()
    result = serializers.JSONField(required=False)
    info = serializers.JSONField(required=False)