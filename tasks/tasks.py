import time
import random
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import TaskResult, EmailTask


@shared_task(bind=True)
def long_running_task(self, duration=10):
    """
    A simple long-running task that simulates work
    """
    task_id = self.request.id
    
    # Save task info to database
    task_result, created = TaskResult.objects.get_or_create(
        task_id=task_id,
        defaults={
            'task_name': 'long_running_task',
            'status': 'STARTED'
        }
    )
    
    try:
        for i in range(duration):
            time.sleep(1)
            # Update progress
            self.update_state(
                state='PROGRESS',
                meta={'current': i + 1, 'total': duration, 'status': f'Processing step {i + 1}'}
            )
        
        result = f"Task completed successfully after {duration} seconds"
        
        # Update database
        task_result.status = 'SUCCESS'
        task_result.result = result
        task_result.save()
        
        return {'current': duration, 'total': duration, 'status': 'Task completed!', 'result': result}
    
    except Exception as exc:
        task_result.status = 'FAILURE'
        task_result.result = str(exc)
        task_result.save()
        raise exc

@shared_task
def add_numbers(x, y):
    """
    Simple addition task
    """
    task_id = add_numbers.request.id if hasattr(add_numbers, 'request') else 'unknown'
    
    TaskResult.objects.create(
        task_id=task_id,
        task_name='add_numbers',
        status='SUCCESS',
        result=f"{x} + {y} = {x + y}"
    )
    
    return x + y

@shared_task
def multiply_numbers(x, y):
    """
    Simple multiplication task with random delay
    """
    delay = random.randint(1, 5)
    time.sleep(delay)
    
    result = x * y
    task_id = multiply_numbers.request.id if hasattr(multiply_numbers, 'request') else 'unknown'
    
    TaskResult.objects.create(
        task_id=task_id,
        task_name='multiply_numbers',
        status='SUCCESS',
        result=f"{x} * {y} = {result} (took {delay}s)"
    )
    
    return result

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 60})
def send_email_task(self, email_id):
    """
    Send email task with retry mechanism
    """
    try:
        email_task = EmailTask.objects.get(id=email_id)
        email_task.task_id = self.request.id
        email_task.save()
        
        # Simulate email sending (replace with actual email sending logic)
        # send_mail(
        #     email_task.subject,
        #     email_task.message,
        #     settings.DEFAULT_FROM_EMAIL,
        #     [email_task.recipient],
        #     fail_silently=False,
        # )
        
        # For demo purposes, simulate random failures
        if random.random() < 0.3:  # 30% chance of failure
            raise Exception("Simulated email sending failure")
        
        time.sleep(2)  # Simulate email sending delay
        
        email_task.is_sent = True
        email_task.save()
        
        TaskResult.objects.create(
            task_id=self.request.id,
            task_name='send_email_task',
            status='SUCCESS',
            result=f"Email sent to {email_task.recipient}"
        )
        
        return f"Email sent successfully to {email_task.recipient}"
    
    except EmailTask.DoesNotExist:
        return "Email task not found"
    except Exception as exc:
        TaskResult.objects.update_or_create(
            task_id=self.request.id,
            defaults={
                'task_name': 'send_email_task',
                'status': 'FAILURE',
                'result': str(exc)
            }
        )
        raise exc

@shared_task
def process_data_batch(data_list):
    """
    Process a batch of data
    """
    processed_items = []
    
    for item in data_list:
        # Simulate processing
        time.sleep(0.5)
        processed_item = {
            'original': item,
            'processed': item.upper() if isinstance(item, str) else item * 2,
            'timestamp': time.time()
        }
        processed_items.append(processed_item)
    
    task_id = process_data_batch.request.id if hasattr(process_data_batch, 'request') else 'unknown'
    
    TaskResult.objects.create(
        task_id=task_id,
        task_name='process_data_batch',
        status='SUCCESS',
        result=f"Processed {len(processed_items)} items"
    )
    
    return processed_items