from django import forms


class SelectDateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d-%m-%Y %H:%M'], label='')
