from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse, HttpResponseBadRequest

from .forms import ReporterSearchForm


@login_required
def search_reporter(request):
    """ ajax request that returns a JSON of queryset containing reporters mailboxes of user by his input"""
    if request.is_ajax():
        form = ReporterSearchForm(data=request.GET)
        if form.is_valid():
            reporter = User.objects.filter(email__contains=form.cleaned_data['reporter'],
                                           profile__in=request.user.profile.get_descendants(include_self=False))[:3]
            if reporter:
                data = serializers.serialize('json', reporter, fields=('email',))
                return JsonResponse(data, safe=False)
            return JsonResponse({'Not Ok': 'Not Found'})
        return JsonResponse({'Not OK': 'invalid data'})
    else:
        return HttpResponseBadRequest()
