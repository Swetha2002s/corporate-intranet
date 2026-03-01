from django import forms
from .models import Ticket, TicketReply, KnowledgeBase


class TicketForm(forms.ModelForm):
    """Form for creating tickets"""
    class Meta:
        model = Ticket
        fields = ['category', 'subject', 'description', 'priority', 'attachment']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ticket subject'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your issue...'
            }),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
        }


class TicketReplyForm(forms.ModelForm):
    """Form for ticket replies"""
    class Meta:
        model = TicketReply
        fields = ['message', 'is_internal']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Add your reply...'
            }),
            'is_internal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class KnowledgeBaseForm(forms.ModelForm):
    """Form for knowledge base articles"""
    class Meta:
        model = KnowledgeBase
        fields = ['title', 'slug', 'content', 'category', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Article title'}),
            'slug': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Article slug'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
