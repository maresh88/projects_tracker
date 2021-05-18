from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Project


class OwnerMixin(LoginRequiredMixin):
    def get_queryset(self):
        qs = super(OwnerMixin, self).get_queryset()
        return qs.filter(author=self.request.user)


class ProjectsListView(OwnerMixin, ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = 'projects'
