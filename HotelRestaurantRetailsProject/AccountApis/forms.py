from HotelApis.models import *
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth import authenticate

from django.conf import settings
from RestaurantApis.models import *

class RegisterNewUserByAdminMyUserForm(UserCreationForm):
    
    
    
    class Meta:
        model = MyUser
        fields = (
        "email",
        "username",
        "password1",
        "password2",
        "phone",
        "UserRole",
        "profile_image",
        #"UserCodes",
        "is_restaurant_user",
        "is_hotel_user",
        "is_retails_user",
        "is_admin",
        # "is_waiter",
        # "is_supervisor",
        "is_paid",

        "AddressLine1",
        "AddressLine2",
        "VatNo",
        "VatEnabled",
        "VatRate",
        "AccountSystem",
        "ApprovedNeeded",
        "SigninTimeout",
        "PrintOrderItems",
        "PrintConfirmedOrderSlip",
        "GridDimensions",
        "StockClosingTime",
        "company_name"

        
         )
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            myuser = MyUser.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} is already exist.")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            myuser = MyUser.objects.get(username=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"username {username} is already exist.")


