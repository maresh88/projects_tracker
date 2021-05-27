from django import forms


class ReporterSearchForm(forms.Form):
    """ Finding User by his email """
    reporter = forms.CharField(max_length=255)
