from django import forms

class ImageForm(forms.Form):
	image = forms.FileField()


class PhotoForm(forms.Form):
	photo = forms.FileField()