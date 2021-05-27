from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """ Comment form on project detail view"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['body'].label = False

    class Meta:
        model = Comment
        fields = ('body', )
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add comment here...'})
        }


