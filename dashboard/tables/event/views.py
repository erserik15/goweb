from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from dashboard.decorators import OwnerRequiredMixin
import django_tables2 as tables
import django_filters
from django_filters.views import FilterView

from dashboard.decorators import group_required
from ecolifestyle.models import *
from .forms import *


@login_required()
@group_required(['event-owner'])
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.owner = request.user
            event.save()
            form.save()
            return JsonResponse({'success': True})
    else:
        form = EventForm(user=request.user)
    return render(request, 'dashboard/tables/form_base.html', {'form': form})

@login_required()
@group_required(['event-owner'])
def event_edit(request, pk):
    event = get_object_or_404(event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=Event)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = EventForm(instance=Event)
    return render(request, 'dashboard/tables/form_base.html', {'form': form, 'edit_url': reverse('dashboard:event_edit', kwargs={'pk': event.pk}) })

@login_required
@group_required(['event-owner'])
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('dashboard:event_index')
    raise Http404

class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = ['id', 'title']
    
class EventTable(tables.Table):
    actions = tables.TemplateColumn(
        '<div class="dropdown">'
            '<button class="btn btn-secondary dropdown-toggle" type="button" '
                'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                'Actions</button>'
                '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
                '<a class="dropdown-item edit-button" data-url="{% url \'dashboard:event_edit\' pk=record.pk %}">Edit</a>'
                '<a class="">'
                    '<form method="post" action="{% url \'dashboard:event_delete\' pk=record.pk %}">'
                        '{% csrf_token %}'
                        '<button class=" delete-button dropdown-item" type="submit">Delete</button>'
                    '</form>'
                '</a>'
            '</div>'
        '</div>',
        verbose_name='Actions'
    )

    class Meta:
        model = Event
        fields = ("id","title","created_at" )
        attrs = {
            'class': 'table table-hover',
        }
        row_attrs = {
            "data-id": lambda record: record.pk
        }

class EventListView(LoginRequiredMixin,OwnerRequiredMixin,tables.SingleTableMixin,FilterView):
    model = Event
    table_class = EventTable
    template_name = 'dashboard/tables/event/index.html'
    paginator_class = tables.LazyPaginator
    filterset_class = EventFilter
    #paginate_by = 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = EventForm()
        context['segment'] = 'event_index'
        return context
    
    def get_queryset(self, *args, **kwargs):
        return Event.objects.filter(owner = self.request.user)