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
@group_required(['post-owner'])
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.owner = request.user
            post.save()
            form.save()
            return JsonResponse({'success': True})
    else:
        form = PostForm(user=request.user)
    return render(request, 'dashboard/tables/form_base.html', {'form': form})

@login_required()
@group_required(['post-owner'])
def post_edit(request, pk):
    post = get_object_or_404(post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=Post)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = PostForm(instance=Post)
    return render(request, 'dashboard/tables/form_base.html', {'form': form, 'edit_url': reverse('dashboard:post_edit', kwargs={'pk': post.pk}) })

@login_required
@group_required(['post-owner'])
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('dashboard:post_index')
    raise Http404

class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = ['id', 'title']
    
class PostTable(tables.Table):
    actions = tables.TemplateColumn(
        '<div class="dropdown">'
            '<button class="btn btn-secondary dropdown-toggle" type="button" '
                'data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'
                'Actions</button>'
                '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">'
                '<a class="dropdown-item edit-button" data-url="{% url \'dashboard:post_edit\' pk=record.pk %}">Edit</a>'
                '<a class="">'
                    '<form method="post" action="{% url \'dashboard:post_delete\' pk=record.pk %}">'
                        '{% csrf_token %}'
                        '<button class=" delete-button dropdown-item" type="submit">Delete</button>'
                    '</form>'
                '</a>'
            '</div>'
        '</div>',
        verbose_name='Actions'
    )

    class Meta:
        model = Post
        fields = ("id","title","created_at" )
        attrs = {
            'class': 'table table-hover',
        }
        row_attrs = {
            "data-id": lambda record: record.pk
        }

class PostListView(LoginRequiredMixin,OwnerRequiredMixin,tables.SingleTableMixin,FilterView):
    model = Post
    table_class = PostTable
    template_name = 'dashboard/tables/post/index.html'
    paginator_class = tables.LazyPaginator
    filterset_class = PostFilter
    #paginate_by = 1
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["form"] = PostForm()
        context['segment'] = 'post_index'
        return context
    
    def get_queryset(self, *args, **kwargs):
        return Post.objects.filter(owner = self.request.user)