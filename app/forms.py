from django import forms
from .models import Urls


# create a ModelForm
class UrlsForm(forms.ModelForm):
    class Meta:
        model = Urls
        exclude = ('shortened_url', 'clicks')