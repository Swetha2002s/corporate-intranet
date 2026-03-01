from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Ticket, TicketReply, TicketCategory, KnowledgeBase
from .forms import TicketForm, TicketReplyForm, KnowledgeBaseForm
from users.models import Profile


@login_required
def ticket_dashboard(request):
    """Ticket management dashboard"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    # Get all tickets
    all_tickets = Ticket.objects.all()
    
    context = {
        'open_tickets': all_tickets.filter(status='open').count(),
        'in_progress_tickets': all_tickets.filter(status='in_progress').count(),
        'resolved_tickets': all_tickets.filter(status='resolved').count(),
        'closed_tickets': all_tickets.filter(status='closed').count(),
        'tickets': all_tickets[:10],
    }
    return render(request, 'tickets/ticket_dashboard.html', context)


class TicketListView(LoginRequiredMixin, ListView):
    """List tickets"""
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 20

    def get_queryset(self):
        try:
            profile = self.request.user.profile
            if profile.role in ['admin', 'hr']:
                return Ticket.objects.all().order_by('-created_at')
        except Profile.DoesNotExist:
            pass
        return Ticket.objects.filter(raised_by=self.request.user).order_by('-created_at')


class TicketDetailView(LoginRequiredMixin, DetailView):
    """View ticket details"""
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = self.get_object().replies.all().order_by('created_at')
        context['form'] = TicketReplyForm()
        return context

    def post(self, request, *args, **kwargs):
        ticket = self.get_object()
        if request.POST.get('action') == 'reply':
            form = TicketReplyForm(request.POST)
            if form.is_valid():
                reply = form.save(commit=False)
                reply.ticket = ticket
                reply.author = request.user
                reply.save()
                ticket.status = 'open'
                ticket.save()
                messages.success(request, 'Reply added')
        return self.get(request, *args, **kwargs)


class TicketCreateView(LoginRequiredMixin, CreateView):
    """Create new ticket"""
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/ticket_form.html'
    success_url = '/tickets/'

    def form_valid(self, form):
        form.instance.raised_by = self.request.user
        try:
            form.instance.department = self.request.user.profile.department
        except:
            pass
        return super().form_valid(form)


@login_required
def assign_ticket(request, pk):
    """Assign ticket to staff (admin/hr only)"""
    ticket = get_object_or_404(Ticket, pk=pk)
    
    try:
        profile = request.user.profile
        if profile.role not in ['admin', 'hr']:
            messages.error(request, 'Permission denied')
            return redirect('ticket-detail', pk=pk)
    except Profile.DoesNotExist:
        messages.error(request, 'Permission denied')
        return redirect('ticket-detail', pk=pk)
    
    if request.method == 'POST':
        assigned_to_id = request.POST.get('assigned_to')
        if assigned_to_id:
            from django.contrib.auth.models import User
            assigned_user = get_object_or_404(User, pk=assigned_to_id)
            ticket.assigned_to = assigned_user
            ticket.status = 'open'
            ticket.save()
            messages.success(request, f'Ticket assigned to {assigned_user.username}')
    
    return redirect('ticket-detail', pk=pk)


@login_required
def resolve_ticket(request, pk):
    """Resolve ticket"""
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if request.method == 'POST':
        ticket.status = 'resolved'
        ticket.resolved_at = timezone.now()
        ticket.resolution_notes = request.POST.get('resolution_notes', '')
        ticket.save()
        messages.success(request, 'Ticket marked as resolved')
    
    return redirect('ticket-detail', pk=pk)


@login_required
def close_ticket(request, pk):
    """Close ticket"""
    ticket = get_object_or_404(Ticket, pk=pk)
    
    if ticket.status == 'resolved':
        ticket.status = 'closed'
        ticket.closed_at = timezone.now()
        ticket.save()
        messages.success(request, 'Ticket closed')
    else:
        messages.error(request, 'Cannot close unresolved ticket')
    
    return redirect('ticket-detail', pk=pk)


class KnowledgeBaseListView(ListView):
    """List knowledge base articles"""
    model = KnowledgeBase
    template_name = 'tickets/kb_list.html'
    context_object_name = 'articles'
    paginate_by = 20

    def get_queryset(self):
        return KnowledgeBase.objects.filter(is_published=True).order_by('-views')


class KnowledgeBaseDetailView(DetailView):
    """View knowledge base article"""
    model = KnowledgeBase
    template_name = 'tickets/kb_detail.html'
    context_object_name = 'article'
    slug_field = 'slug'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.object.views += 1
        self.object.save()
        return response
