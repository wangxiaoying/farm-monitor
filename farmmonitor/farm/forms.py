from django import forms

class PhotoForm(forms.Form):
	photo = forms.FileField()