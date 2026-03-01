from django.urls import path
from . import views

urlpatterns = [
    # Tickets
    path('', views.ticket_dashboard, name='ticket-dashboard'),
    path('tickets/', views.TicketListView.as_view(), name='ticket-list'),
    path('ticket/new/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('ticket/<int:pk>/assign/', views.assign_ticket, name='ticket-assign'),
    path('ticket/<int:pk>/resolve/', views.resolve_ticket, name='ticket-resolve'),
    path('ticket/<int:pk>/close/', views.close_ticket, name='ticket-close'),
    
    # Knowledge Base
    path('kb/', views.KnowledgeBaseListView.as_view(), name='kb-list'),
    path('kb/<slug:slug>/', views.KnowledgeBaseDetailView.as_view(), name='kb-detail'),
]
