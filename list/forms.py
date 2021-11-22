from django.forms import ModelForm
from django import forms
from .models import Contact, Event

class EditForm(ModelForm):
    class Meta:

        model = Contact
        fields = ["contact_name", "contact_organisation", "contact_email", "contact_mobile","startlist","results", "communiques"]
        labels = {
            'contact_name': 'Name',
            'contact_organisation': 'Organisation',
            'contact_email': 'Email',
            'contact_mobile': 'Mobile',
            'startlist': 'Startlist',
            'results': 'Results',
            'communiques': 'Communiques',
        }
        instance = Contact

class sendForm(ModelForm):
    URL = forms.CharField(label='URL', required=True)
    Options = (
        ("",""),
        ("startlist", "startlist"),
        ("results", "results"),
        ("communiques", "communiques"),)
    email_option = forms.ChoiceField(choices=Options)
    stagenumber = forms.CharField(required=False)
    comment = forms.CharField(widget=forms.Textarea(attrs={"rows": 20, "cols": 50}),required=False)
    class Meta:
        model = Contact
        fields = ["event"]



