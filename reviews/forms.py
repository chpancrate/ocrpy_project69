from django import forms
from reviews.models import Ticket, Review, UserFollows


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']


class FollowUserForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']
