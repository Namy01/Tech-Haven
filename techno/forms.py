from django import forms
from .models import Review, Newsletter


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"


class NewsletterForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = "__all__"