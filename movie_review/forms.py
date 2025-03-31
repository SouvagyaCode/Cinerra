from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f"{i} ⭐") for i in range(1, 11)],
        widget=forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ['rating', 'review_text']
