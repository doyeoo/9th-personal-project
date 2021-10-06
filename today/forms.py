from django import forms
import datetime
from .models import *

class ScheduleForm(forms.ModelForm):
    class Meta:
        model=Schedule
        fields=('start_time', 'end_time', 'contents')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'message')