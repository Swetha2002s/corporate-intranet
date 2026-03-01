from django.db import models
from django.contrib.auth.models import User
from users.models import Department
import uuid


class TicketCategory(models.Model):
    """Categories for tickets (IT, HR, Admin, etc.)"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Ticket Categories"

    def __str__(self):
        return self.name


class Ticket(models.Model):
    """Support/Help Desk Tickets"""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('waiting_customer', 'Waiting for Customer'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('reopened', 'Reopened'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    SLA_CHOICES = [
        ('4', '4 Hours'),
        ('8', '8 Hours'),
        ('24', '24 Hours'),
        ('48', '48 Hours'),
    ]

    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    
    category = models.ForeignKey(TicketCategory, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    
    raised_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='raised_tickets')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='assigned_tickets')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    sla = models.CharField(max_length=5, choices=SLA_CHOICES, default='24')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    
    resolution_notes = models.TextField(blank=True)
    attachment = models.FileField(upload_to='tickets/%Y/%m/', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            import datetime
            self.ticket_id = f"TKT-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_id} - {self.subject}"


class TicketReply(models.Model):
    """Replies/Updates on tickets"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_internal = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Reply to {self.ticket.ticket_id} by {self.author.username}"


class KnowledgeBase(models.Model):
    """FAQ and Help articles"""
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    category = models.ForeignKey(TicketCategory, on_delete=models.SET_NULL, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    is_published = models.BooleanField(default=True)
    views = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Knowledge Base Articles"
        ordering = ['-updated_at']

    def __str__(self):
        return self.title
