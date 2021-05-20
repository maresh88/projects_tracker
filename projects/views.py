from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin

from .models import Project
from .forms import CommentForm


class OwnerMixin(LoginRequiredMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class OwnerAndManagerMixin(LoginRequiredMixin):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author__profile__in=self.request.user.profile.get_descendants(include_self=True))


class OwnerMixinEdit(OwnerMixin):
    model = Project
    template_name = 'projects/project_create_update.html'
    fields = ['title', 'description', 'project_status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(OwnerMixinEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})


class ProjectsListView(OwnerAndManagerMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'

    def get_queryset(self):
        return super(ProjectsListView, self).get_queryset().annotate(Count('comments', distinct=True)).order_by(
            '-created_at')


class ProjectCreateView(OwnerMixinEdit, CreateView):
    pass


class ProjectUpdateView(OwnerMixinEdit, UpdateView):
    pass


class ProjectDisplay(DetailView):
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


class ProjectDetailView(OwnerAndManagerMixin, View):

    def get(self, request, *args, **kwargs):
        view = ProjectDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = ProjectComments.as_view()
        return view(request, *args, **kwargs)
