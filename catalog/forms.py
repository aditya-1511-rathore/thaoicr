from django import forms
from .models import OCRResult

class OCRForm(forms.ModelForm):
    class Meta:
        model = OCRResult
        fields = ['image']
