from django import forms
from django import views
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)


class GenerateAddressForm(forms.Form):

    bitcoin_address = forms.CharField(label="Bitcoin generated Address")
    # public_key_address = forms.CharField(label="Bitcoin generated Public Key")
    # private_key_address = forms.CharField(label="Bitcoin generated Private Key")


class TransferAmountForm(forms.Form):

    from_address = forms.CharField(label="From Address", required=True)
    send_to_address = forms.CharField(label="To Address", required=True)
    amount_field = forms.IntegerField(label="Amount", required=True)