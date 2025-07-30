from django.db import models

class TaskResult(models.Model):
    TASK_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('STARTED', 'Started'),
        ('SUCCESS', 'Success'),
        ('FAILURE', 'Failure'),
        ('RETRY', 'Retry'),
        ('REVOKED', 'Revoked'),
    ]
    
    task_id = models.CharField(max_length=255, unique=True)
    task_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=TASK_STATUS_CHOICES, default='PENDING')
    result = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.task_name} - {self.status}"

class EmailTask(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    task_id = models.CharField(max_length=255, blank=True, null=True)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Email to {self.recipient}: {self.subject}"