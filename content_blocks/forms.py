from django import forms

from content_blocks.models import ContentBlock


class ContentBlockForm(forms.ModelForm):
    """
    A simple edit form for the ContentBlock model
    """
    class Meta:
        model = ContentBlock
        fields = ("content", )
