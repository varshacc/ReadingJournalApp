from django import forms
from .models import Task,Thought
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})
# Reordering Form and View

from ReadingJournalApp import settings
class PositionForm(forms.Form):
    position = forms.CharField()
    startDate = forms.DateField(widget=DateInput(), input_formats= settings.DATE_INPUT_FORMATS)
    endDate = forms.DateField(widget=DateInput(), input_formats= settings.DATE_INPUT_FORMATS)
    rating = forms.ChoiceField(choices=Task.RATING_RANGE)

class ThoughtForm(forms.Form):
    highlights = forms.CharField(max_length=100)