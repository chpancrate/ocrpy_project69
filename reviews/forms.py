from django import forms
from django.forms import widgets
from reviews.models import Ticket, Review, UserFollows
from django.contrib.auth import get_user_model


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['image'].widget.attrs['class'] = 'form-control'


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'body', 'rating']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        RATING_CHOICES = [
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 4),
            (5, 5),
        ]
        self.fields['headline'].widget.attrs['class'] = 'form-control'
        self.fields['body'].widget.attrs['class'] = 'form-control'
        self.fields['rating'] = forms.ChoiceField(
            choices=RATING_CHOICES,
            widget=widgets.RadioSelect(
                attrs={'class': 'form-check-input'})
                )


class FollowUserForm(forms.ModelForm):
    class Meta:
        model = UserFollows
        fields = ['followed_user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['followed_user'] = forms.CharField(
            widget=widgets.TextInput(
                attrs={'class': 'form-control'})
                )

    def clean_followed_user(self):
        User = get_user_model()
        username = self.cleaned_data['followed_user']
        user = User.objects.filter(username=username)
        if len(user) == 0 :
            raise forms.ValidationError("Utilisateur inconnu")
        else:
            return user[0]
