from django import forms
from .models import *


class RobotForm(forms.Form):

    class Meta:
        model = Robot
        fields = ['model ', 'version', 'created']

