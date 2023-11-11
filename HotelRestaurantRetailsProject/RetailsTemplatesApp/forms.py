from HotelApis.models import *
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth import authenticate

from django.conf import settings
from RetailsApis.models import *

class MyUserForm(UserCreationForm):
    
    
    
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
        "is_retails_user",
        "is_waiter",
        "is_supervisor",
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


# class LoginAuthenticationForm(AuthenticationForm):
#     class Meta:
#         model = MyUser
#         fields = ['email','password1','UserCodes']



class UpdateMyUserForm(forms.ModelForm):
    
    
    class Meta:
        model = MyUser
        fields = (
        "email",
        "username",
        "phone",
        "UserRole",
        "profile_image",
        "is_retails_user",
        "is_waiter",
        "is_supervisor",
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

class PasswordChangingForm(PasswordChangeForm):

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'New Passowrd'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Conform new password'}))
    class Meta:
        model = MyUser
        fields = ['old_password', 'new_password1', 'new_password2']







class RetailsCustomersSearchForm(forms.ModelForm):
    
    CustomerFullName = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'customer', 'placeholder' : 'Enter Customer Name'})

    )

    CustomerAddress = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'address', 'placeholder' : 'Enter Customer Address'})

    )
    


    class Meta:
        model = RetailsCustomers
        fields =['CustomerFullName','CustomerAddress']




class AddRetailsCustomerForm(forms.ModelForm):
    class Meta:
        model = RetailsCustomers
        fields ='__all__'






#---------------------BUSINESS UNIT-----------------
class RetailsBusinessUnitSearchForm(forms.ModelForm):
    
    Code = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'code', 'placeholder' : 'Enter Business Unit Code'})

    )

    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = RetailsBusinessUnit
        fields =['Code','Description']




class AddRetailsBusinessUnitForm(forms.ModelForm):
    class Meta:
        model = RetailsBusinessUnit
        fields ='__all__'






#---------------------LOCATION CODES-----------------
class RetailsLocationCodeSearchForm(forms.ModelForm):
    
    Code = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'code', 'placeholder' : 'Enter Business Unit Code'})

    )

    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = RetailsLocationCode
        fields =['Code','Description','BusinessUnit']




class AddRetailsLocationCodeForm(forms.ModelForm):
    class Meta:
        model = RetailsLocationCode
        fields ='__all__'




#---------------------PROCESS CONFIG-----------------
class RetailsProcessConfigSearchForm(forms.ModelForm):
    
    ProcesId = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'ProcessId', 'placeholder' : 'Enter Process Id'})

    )

    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = RetailsProcessConfig
        fields =['ProcesId','Description']




class AddRetailsProcessConfigForm(forms.ModelForm):
    class Meta:
        model = RetailsProcessConfig
        fields ='__all__'







#---------------------Retails STORE CODES-----------------
class RetailsStoreCodeSearchForm(forms.ModelForm):
    
    Code = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'code', 'placeholder' : 'Enter Store Code'})

    )

    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = RetailsStoreCode
        fields =['Code','Description','Location','Process']




class AddRetailsStoreCodeForm(forms.ModelForm):
    class Meta:
        model = RetailsStoreCode
        fields ='__all__'













#---------------------Retails STORE BIN CODES-----------------
class RetailsStoreBinCodeSearchForm(forms.ModelForm):
    
    StoreBinCode = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'StoreBinCode', 'placeholder' : 'Enter Store Bin Code'})

    )

    CardNo = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'CardNo', 'placeholder' : 'Enter CardNo'})

    )


    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = RetailsStoreBinCode
        fields =['StoreBinCode','Description','CardNo']




class AddRetailsStoreBinCodeForm(forms.ModelForm):
    class Meta:
        model = RetailsStoreBinCode
        fields ='__all__'






#----------------EVENT CODE--------------------------
class RetailsEventCodeSearchForm(forms.ModelForm):
    
    Code = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'code', 'placeholder' : 'Enter Event Code'})

    )

    Description = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'desription', 'placeholder' : 'Description'})

    )
    


    class Meta:
        model = RetailsEventCode
        fields =['Code','Description']



class AddRetailsEventCodeForm(forms.ModelForm):
    class Meta:
        model = RetailsEventCode
        fields ='__all__'






class RetailsEventAlertSearchForm(forms.ModelForm):
    
    AlertID = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'AlertID', 'placeholder' : 'Enter AlertID'})

    )

    
    


    class Meta:
        model = RetailsEventAlert
        fields =['AlertID']



class AddRetailsEventAlertForm(forms.ModelForm):
    class Meta:
        model = RetailsEventAlert
        fields ='__all__'









#-------------------Retails UOM------------------------------
class RetailsUOMSearchForm(forms.ModelForm):
    
    UOMShortCode = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'UOMShortCode', 'placeholder' : 'Enter UOM Short Code'})

    )

        


    class Meta:
        model = RetailsUOM
        fields =['UOMShortCode']




class AddRetailsUOMForm(forms.ModelForm):
    class Meta:
        model = RetailsUOM
        fields ='__all__'







#-------------------Retails BOM------------------------------
class RetailsBOMSearchForm(forms.ModelForm):
    
    Code = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'code', 'placeholder' : 'BOM Code'})

    )

    Name = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'Name', 'placeholder' : 'Name'})

    )

        


    class Meta:
        model = RetailsBOM
        fields =['Code','Name']




class AddRetailsBOMForm(forms.ModelForm):
    class Meta:
        model = RetailsBOM
        fields ='__all__'



#----------UPLOAD BOM FILE-------------------
class AddRetailsBOMFilesForm(forms.ModelForm):
    class Meta:
        model = RetailsBOMFiles
        fields ='__all__'




#----------Retails  PRODUCTS CATEGORIES-------------------
class AddRetailsCategoriesForm(forms.ModelForm):
    class Meta:
        model = RetailsCategories
        fields ='__all__'



class AddRoomsClassesForm(forms.ModelForm):
    class Meta:
        model = RoomsClasses
        fields ='__all__'






















#-------------------Retails  PRODUCTS------------------------------
class RetailsProductsSearchForm(forms.ModelForm):
    
    product_name = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'product_name'})

    )

    product_second_name = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'product_second_name'})

    )

        
    class Meta:
        model = RetailsProducts
        fields =['product_name','product_second_name','productCategory']



class AddRetailsProductsForm(forms.ModelForm):
    class Meta:
        model = RetailsProducts
        fields ='__all__'





































#-------------------------UPLOAD PRODUCTS-------------------

class UploadRetailsProductsForm(forms.ModelForm):
    class Meta:
        model = RetailsProducts
        fields ='__all__'
        








#------------------------Retails  SEARCH ORDERS---------------
# class RetailsOrderSearchForm(forms.ModelForm):


         
#     class Meta:
#         model = RetailsOrder
#         fields =['user']

class RetailsOrderSearchForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'datepicker'}))

    end_date = forms.DateTimeField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'datepicker'}))

    export_to_CSV = forms.BooleanField(required=False)

    
         
    class Meta:
        model = RetailsOrder
        fields =['user','start_date','end_date']
        #fields =['user']



















class RetailsMyUserSearchForm(forms.ModelForm):
    
    username = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'username'})

    )

    email = forms.EmailField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'email'})

    )

        


    class Meta:
        model = MyUser
        fields =['username','email']









#-------------------Retails SUPPLIER MAINTENANCE--------------

class RetailsSuppliersSearchForm(forms.ModelForm):
    
    SupplierFullName = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'supplier'})

    )


    Keyword = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'keyword'})

    )

    

        
    class Meta:
        model = RetailsSuppliers
        fields =['SupplierFullName', 'Keyword','Status']



class AddRetailsSuppliersForm(forms.ModelForm):
    class Meta:
        model = RetailsSuppliers
        fields ='__all__'













#-----------------UNPAID Retails USERS--------------------

class UnpaidRetailsMyUserSearchForm(forms.ModelForm):
    
    username = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'username'})

    )

    email = forms.EmailField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'email'})

    )

    company_name = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'company_name'})

    )
    


    class Meta:
        model = MyUser
        fields =['email','username','company_name']



#------------UPDATE UNPAID Retails USERS--------------
class UpdateUnpaidRetailsMyUserForm(forms.ModelForm):
    
    class Meta:
        model = MyUser
        fields =['is_active','is_paid']






#-----------------PAID Retails USERS--------------------

class paidRetailsMyUserSearchForm(forms.ModelForm):
    
    username = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'username'})

    )

    email = forms.EmailField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'email'})

    )

    company_name = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'company_name'})

    )
    


    class Meta:
        model = MyUser
        fields =['email','username','company_name']



#------------UPDATE UNPAID Retails USERS--------------
class UpdatepaidRetailsMyUserForm(forms.ModelForm):
    
    class Meta:
        model = MyUser
        fields =['is_active','is_paid']

