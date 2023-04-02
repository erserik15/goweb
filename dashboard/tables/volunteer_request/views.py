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
@group_required(['volunteer_request-owner'])
def volunteer_request_create(request):
    if request.method == 'POST':
        form = VolunteerRequestForm(request.POST, request.FILES)
        if form.is_valid():
            volunteer_request = form.save(commit=False)
            volunteer_request.owner = request.user
            volunteer_request.save()
            form.save()
            return JsonResponse({'success': True})
    else:
        form = VolunteerRequestForm(user=request.user)
    return render(request, 'dashboard/tables/form_base.html', {'form': form})

@login_required()
@group_required(['volunteer_request-owner'])
def volunteer_request_edit(request, pk):
    volunteer_request = get_object_or_404(volunteer_request, pk=pk)
    if request.method == 'POST':
        form = VolunteerRequestForm(request.POST, request.FILES, instance=VolunteerRequest)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = VolunteerRequestForm(instance=VolunteerRequest)
    return render(request, 'dashboard/tables/form_base.html', {'form': form, 'edit_url': reverse('dashboard:volunteer_request_edit', kwargs={'pk': volunteer_request.pk}) })

@login_required
@group_required(['volunteer_request-owner'])
def volunteer_request_delete(request, pk):
    volunteer_request = get_object_or_404(VolunteerRequest, pk=pk)
    if request.method == 'POST':
        volunteer_request.delete()
        return redirect('dashboard:volunteer_request_index')
    raise Http404

class VolunteerRequestFilter(django_filters.FilterSet):
    class Meta:
        model = VolunteerRequest
        fields = ['id', 'name','email']
    
class VolunteerRequestTable(tables.Table):
    actions = tables.TemplateColumn(
        '<div class="dropdown">'
            '<button class="btn btn-secondary dropdown-toggle" type="button" '
                'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                'Actions</button>'
                '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
                '<a class="dropdown-item edit-button" data-url="{% url \'dashboard:volunteer_request_edit\' pk=record.pk %}">Edit</a>'
                '<a class="">'
                    '<form method="post" action="{% url \'dashboard:volunteer_request_delete\' pk=record.pk %}">'
                        '{% csrf_token %}'
                        '<button class=" delete-button dropdown-item" type="submit">Delete</button>'
                    '</form>'
                '</a>'
            '</div>'
        '</div>',
        verbose_name='Actions'
    )

    class Meta:
        model = VolunteerRequest
        fields = ("id","name","email","created_at" )
        attrs = {
            'class': 'table table-hover',
        }
        row_attrs = {
            "data-id": lambda record: record.pk
        }

class VolunteerRequestListView(LoginRequiredMixin,OwnerRequiredMixin,tables.SingleTableMixin,FilterView):
    model = VolunteerRequest
    table_class = VolunteerRequestTable
    template_name = 'dashboard/tables/volunteer_request/index.html'
    paginator_class = tables.LazyPaginator
    filterset_class = VolunteerRequestFilter
    #paginate_by = 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = VolunteerRequestForm()
        context['segment'] = 'volunteer_request_index'
        return context
    
    def get_queryset(self, *args, **kwargs):
        return VolunteerRequest.objects.filter(owner = self.request.user)