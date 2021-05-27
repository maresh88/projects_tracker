from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse
from django.views import View
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  UpdateView)
from django.views.generic.detail import SingleObjectMixin

from .forms import CommentForm
from .models import Project


class OwnerMixin(LoginRequiredMixin):
    """Get user projects"""
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class ManagerAndReportersMixin(LoginRequiredMixin):
    """Get all projects that user have access to, including user reporters projects through mptt"""
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author__profile__in=self.request.user.profile.get_descendants(include_self=True))


class OwnerMixinEdit(OwnerMixin):
    """Mixin that allows only the project's author to make changes and create a new one"""
    model = Project
    template_name = 'projects/project_create_update.html'
    fields = ['title', 'description', 'project_status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(OwnerMixinEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})


class ProjectsListView(ManagerAndReportersMixin, ListView):
    """Get list of projects"""
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProjectsListView, self).get_context_data()

        # collect available choices from Project model
        context['filter_status'] = Project._meta.get_field('project_status').choices
        return context

    def get_queryset(self):
        """Get projects with the number of comments for each of them"""
        return super(ProjectsListView, self).get_queryset().annotate(Count('comments', distinct=True)).order_by(
            '-created_at')


class ProjectCreateView(OwnerMixinEdit, CreateView):
    pass


class ProjectUpdateView(OwnerMixinEdit, UpdateView):
    pass


class ProjectDisplay(DetailView):
    """Get project view with comments"""
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDisplay, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def get_queryset(self):
        return super(ProjectDisplay, self).get_queryset().prefetch_related('comments', 'comments__author')


class ProjectComments(SingleObjectMixin, FormView):
    """Leave a comment on project view"""
    model = Project
    template_name = 'projects/project_detail.html'
    form_class = CommentForm

    def form_valid(self, form):
        comment = form.save(commit=False)
        self.obj = self.get_object()
        comment.project = self.obj
        comment.author = self.request.user
        comment.save()
        return super(ProjectComments, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.obj.pk, 'slug': self.obj.slug})


class ProjectDetailView(ManagerAndReportersMixin, View):

    def get(self, request, *args, **kwargs):
        view = ProjectDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProjectComments.as_view()
        return view(request, *args, **kwargs)


class ProjectFilterView(ProjectsListView):
    """Filtering projects by year, status and author"""
    def get_queryset(self):
        author = self.request.GET.get('reporter')
        if not author:
            author = self.request.user.email
        qs = super(ProjectFilterView, self).get_queryset().filter(author__email=author,
                                                                  project_status__in=self.request.GET.getlist('status'),
                                                                  created_at__year__in=self.request.GET.getlist('year'))
        return qs

