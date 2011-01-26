from .models import SimplePage
from django.forms import ModelForm



class SimplePageForm(ModelForm):

    class Meta:
        model = SimplePage
        fields = ['content']


