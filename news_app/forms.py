from django import forms
from .models import Contact, Comments

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = '__all__'


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = [ 'body',]