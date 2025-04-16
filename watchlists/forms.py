from django import forms
from .models import Watchlist, WatchlistItem

class WatchlistForm(forms.ModelForm):
    class Meta:
        model = Watchlist
        fields = ['name', 'description', 'privacy', 'collaborators']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class WatchlistItemForm(forms.ModelForm):
    class Meta:
        model = WatchlistItem
        fields = ['movie', 'status', 'priority', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
            'movie': forms.HiddenInput(),
        }

class WatchlistItemUpdateForm(forms.ModelForm):
    class Meta:
        model = WatchlistItem
        fields = ['status', 'priority', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 2}),
        }