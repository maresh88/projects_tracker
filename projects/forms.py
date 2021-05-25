from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = False

    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add comment here...'})
        }


class SearchForm(forms.Form):
    reporter = forms.CharField(max_length=255)