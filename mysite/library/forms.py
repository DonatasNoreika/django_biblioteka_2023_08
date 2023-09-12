from .models import BookReview, Profilis, BookInstance
from django import forms
from django.contrib.auth.models import User


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['content']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']


class DateInput(forms.DateInput):
    input_type = "date"


class UserBooksCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'due_back', 'status']
        widgets = {'due_back': DateInput()}
