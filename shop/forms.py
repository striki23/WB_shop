from django import forms

from shop.models import Review


class AddReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['stars', 'text']
        widgets = {
            'stars': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }
