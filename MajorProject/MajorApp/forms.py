from django import forms

from crispy_forms.helper import FormHelper

from MajorApp.models import UrlModel

# Forms
class UrlForm(forms.ModelForm):
    class Meta():
        model = UrlModel
        fields = ['url']
