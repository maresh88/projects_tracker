from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .models import Project


class OwnerMixin(LoginRequiredMixin):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(author=self.request.user)


class OwnerMixinEdit(OwnerMixin):
    model = Project
    template_name = 'projects/project_create_update.html'
    fields = ['title', 'description', 'project_status']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(OwnerMixinEdit, self).form_valid(form)

    def get_success_url(self):
        return reverse('projects:detail', kwargs={'pk': self.object.pk, 'slug': self.object.slug})


class ProjectsListView(OwnerMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'


class ProjectCreateView(OwnerMixinEdit, CreateView):
    pass


class ProjectUpdateView(OwnerMixinEdit, UpdateView):
    pass


class ProjectDetailView(OwnerMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'projects/project_detail.html'
