from django import forms
from .models import Review, ReviewComment, ReviewVote

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'title', 'content', 'watch_status',
            'story_rating', 'acting_rating', 'cinematography_rating'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
            'story_rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'acting_rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'cinematography_rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

class ReviewCommentForm(forms.ModelForm):
    class Meta:
        model = ReviewComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Add your comment...'}),
        }

class ReviewVoteForm(forms.ModelForm):
    class Meta:
        model = ReviewVote
        fields = ['helpful']