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
@group_required(['admin'])
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.owner = request.user
            user.save()
            form.save()
            return JsonResponse({'success': True})
    else:
        form = UserForm(user=request.user)
    return render(request, 'dashboard/tables/form_base.html', {'form': form})

@login_required()
@group_required(['admin'])
def user_edit(request, pk):
    user = get_object_or_404(user, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=User)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = UserForm(instance=User)
    return render(request, 'dashboard/tables/form_base.html', {'form': form, 'edit_url': reverse('dashboard:user_edit', kwargs={'pk': user.pk}) })

@login_required
@group_required(['admin'])
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('dashboard:user_index')
    raise Http404

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['id', 'email']
    
class UserTable(tables.Table):
    actions = tables.TemplateColumn(
        '<div class="dropdown">'
            '<button class="btn btn-secondary dropdown-toggle" type="button" '
                'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                'Actions</button>'
                '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
                '<a class="dropdown-item edit-button" data-url="{% url \'dashboard:user_edit\' pk=record.pk %}">Edit</a>'
                '<a class="">'
                    '<form method="post" action="{% url \'dashboard:user_delete\' pk=record.pk %}">'
                        '{% csrf_token %}'
                        '<button class=" delete-button dropdown-item" type="submit">Delete</button>'
                    '</form>'
                '</a>'
            '</div>'
        '</div>',
        verbose_name='Actions'
    )

    class Meta:
        model = User
        fields = ("id","username","email")
        attrs = {
            'class': 'table table-hover',
        }
        row_attrs = {
            "data-id": lambda record: record.pk
        }

class UserListView(LoginRequiredMixin,OwnerRequiredMixin,tables.SingleTableMixin,FilterView):
    model = User
    table_class = UserTable
    template_name = 'dashboard/tables/user/index.html'
    paginator_class = tables.LazyPaginator
    filterset_class = UserFilter
    #paginate_by = 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = UserForm()
        context['segment'] = 'user_index'
        return context
    
    def get_queryset(self, *args, **kwargs):
        return User.objects.all()