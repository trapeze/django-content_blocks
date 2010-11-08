from django import forms

from content_blocks.models import ContentBlock, ImageBlock


class ContentBlockForm(forms.ModelForm):
    """
    A simple edit form for the ContentBlock model
    """
    class Meta:
        model = ContentBlock
        fields = ("content", )


class ImageBlockForm(forms.ModelForm):
    """
    A simple edit form for the ImageBlock model
    """
    class Meta:
        model = ImageBlock
        fields = ('image', 'alternate_text', 'link')
