from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from celery.result import AsyncResult
from django.conf import settings

from .models import TaskResult, EmailTask
from .serializers import (
    TaskResultSerializer, EmailTaskSerializer, LongRunningTaskSerializer,
    AddNumbersSerializer, MultiplyNumbersSerializer, ProcessDataSerializer,
    TaskStatusSerializer
)
from .tasks import long_running_task, add_numbers, multiply_numbers, send_email_task, process_data_batch


class TaskResultListView(generics.ListAPIView):
    """List all task results"""
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer

class TaskResultDetailView(generics.RetrieveAPIView):
    """Get specific task result"""
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    lookup_field = 'task_id'

class EmailTaskListCreateView(generics.ListCreateAPIView):
    """List and create email tasks"""
    queryset = EmailTask.objects.all()
    serializer_class = EmailTaskSerializer

@api_view(['POST'])
def start_long_task(request):
    """Start a long-running task"""
    serializer = LongRunningTaskSerializer(data=request.data)
    if serializer.is_valid():
        duration = serializer.validated_data['duration']
        task = long_running_task.delay(duration)
        return Response({
            'task_id': task.id,
            'status': 'Task started',
            'duration': duration
        }, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def add_task(request):
    """Add two numbers asynchronously"""
    serializer = AddNumbersSerializer(data=request.data)
    if serializer.is_valid():
        x = serializer.validated_data['x']
        y = serializer.validated_data['y']
        task = add_numbers.delay(x, y)
        return Response({
            'task_id': task.id,
            'status': 'Task started',
            'operation': f'{x} + {y}'
        }, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def multiply_task(request):
    """Multiply two numbers asynchronously"""
    serializer = MultiplyNumbersSerializer(data=request.data)
    if serializer.is_valid():
        x = serializer.validated_data['x']
        y = serializer.validated_data['y']
        task = multiply_numbers.delay(x, y)
        return Response({
            'task_id': task.id,
            'status': 'Task started',
            'operation': f'{x} * {y}'
        }, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def send_email(request):
    """Send email asynchronously"""
    serializer = EmailTaskSerializer(data=request.data)
    if serializer.is_valid():
        email_task = serializer.save()
        task = send_email_task.delay(email_task.id)
        email_task.task_id = task.id
        email_task.save()
        
        return Response({
            'task_id': task.id,
            'email_id': email_task.id,
            'status': 'Email task started',
            'recipient': email_task.recipient
        }, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def process_data(request):
    """Process data batch asynchronously"""
    serializer = ProcessDataSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data['data']
        task = process_data_batch.delay(data)
        return Response({
            'task_id': task.id,
            'status': 'Data processing started',
            'items_count': len(data)
        }, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def task_status(request, task_id):
    """Get task status and result"""
    try:
        task_result = AsyncResult(task_id)
        
        response_data = {
            'task_id': task_id,
            'status': task_result.status,
        }
        
        if task_result.state == 'PENDING':
            response_data['info'] = 'Task is waiting to be processed'
        elif task_result.state == 'PROGRESS':
            response_data['info'] = task_result.info
        elif task_result.state == 'SUCCESS':
            response_data['result'] = task_result.result
        elif task_result.state == 'FAILURE':
            response_data['error'] = str(task_result.info)
        
        # Also try to get from database
        try:
            db_task = TaskResult.objects.get(task_id=task_id)
            response_data['db_status'] = db_task.status
            response_data['db_result'] = db_task.result
            response_data['created_at'] = db_task.created_at
        except TaskResult.DoesNotExist:
            pass
        
        return Response(response_data)
    
    except Exception as e:
        return Response({
            'error': f'Error retrieving task: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def cancel_task(request, task_id):
    """Cancel a running task"""
    try:
        from drf_celery_project.celery import app
        app.control.revoke(task_id, terminate=True)
        
        # Update database if exists
        try:
            task_result = TaskResult.objects.get(task_id=task_id)
            task_result.status = 'REVOKED'
            task_result.save()
        except TaskResult.DoesNotExist:
            pass
        
        return Response({
            'task_id': task_id,
            'status': 'Task cancelled'
        })
    
    except Exception as e:
        return Response({
            'error': f'Error cancelling task: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def celery_status(request):
    """Get Celery worker status"""
    try:
        from drf_celery_project.celery import app
        inspect = app.control.inspect()
        
        stats = inspect.stats()
        active_tasks = inspect.active()
        registered_tasks = inspect.registered()
        
        return Response({
            'workers': list(stats.keys()) if stats else [],
            'active_tasks_count': sum(len(tasks) for tasks in active_tasks.values()) if active_tasks else 0,
            'registered_tasks_count': sum(len(tasks) for tasks in registered_tasks.values()) if registered_tasks else 0,
            'broker_url': settings.CELERY_BROKER_URL,
            'result_backend': settings.CELERY_RESULT_BACKEND,
        })
    
    except Exception as e:
        return Response({
            'error': f'Error getting Celery status: {str(e)}',
            'message': 'Make sure Celery worker is running'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)