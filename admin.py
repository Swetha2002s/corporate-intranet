from django.contrib import admin
from .models import TicketCategory, Ticket, TicketReply, KnowledgeBase


@admin.register(TicketCategory)
class TicketCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    search_fields = ['name']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'subject', 'category', 'raised_by', 'assigned_to', 'status', 'priority']
    list_filter = ['status', 'priority', 'category', 'created_at']
    search_fields = ['ticket_id', 'subject', 'description']
    readonly_fields = ['ticket_id', 'created_at', 'updated_at']


@admin.register(TicketReply)
class TicketReplyAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'author', 'created_at', 'is_internal']
    list_filter = ['created_at', 'is_internal']
    search_fields = ['message']
    readonly_fields = ['created_at']


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'is_published', 'views']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
