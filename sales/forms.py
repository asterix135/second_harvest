from django import forms
from django.contrib.auth.models import User
from .models import *

class TicketInputForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ('tick_id', 'tick_type')


class DonorInputForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ('first_name',
                  'last_name',
                  'email',
                  'phone',
                  'address',
                  'city',
                  'province',
                  'postal_code',
                  'opt_out',
)

class EmailCheckForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ('email',)
