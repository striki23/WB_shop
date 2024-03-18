from django import forms

from shop.models import Review


class AddReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['stars', 'text', 'image']
        widgets = {
            'stars': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
