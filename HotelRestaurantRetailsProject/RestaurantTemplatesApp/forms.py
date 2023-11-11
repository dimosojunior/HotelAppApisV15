from HotelApis.models import *
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,PasswordChangeForm, UserChangeForm
from django.contrib.auth import authenticate

from django.conf import settings
from RestaurantApis.models import *

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
        "is_restaurant_user",
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
        "is_restaurant_user",
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







class RestaurantCustomersSearchForm(forms.ModelForm):
    
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
        model = RestaurantCustomers
        fields =['CustomerFullName','CustomerAddress']




class AddRestaurantCustomerForm(forms.ModelForm):
    class Meta:
        model = RestaurantCustomers
        fields ='__all__'






#---------------------BUSINESS UNIT-----------------
class RestaurantBusinessUnitSearchForm(forms.ModelForm):
    
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
        model = RestaurantBusinessUnit
        fields =['Code','Description']




class AddRestaurantBusinessUnitForm(forms.ModelForm):
    class Meta:
        model = RestaurantBusinessUnit
        fields ='__all__'






#---------------------LOCATION CODES-----------------
class RestaurantLocationCodeSearchForm(forms.ModelForm):
    
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
        model = RestaurantLocationCode
        fields =['Code','Description','BusinessUnit']




class AddRestaurantLocationCodeForm(forms.ModelForm):
    class Meta:
        model = RestaurantLocationCode
        fields ='__all__'




#---------------------PROCESS CONFIG-----------------
class RestaurantProcessConfigSearchForm(forms.ModelForm):
    
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
        model = RestaurantProcessConfig
        fields =['ProcesId','Description']




class AddRestaurantProcessConfigForm(forms.ModelForm):
    class Meta:
        model = RestaurantProcessConfig
        fields ='__all__'







#---------------------Restaurant STORE CODES-----------------
class RestaurantStoreCodeSearchForm(forms.ModelForm):
    
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
        model = RestaurantStoreCode
        fields =['Code','Description','Location','Process']




class AddRestaurantStoreCodeForm(forms.ModelForm):
    class Meta:
        model = RestaurantStoreCode
        fields ='__all__'













#---------------------Restaurant STORE BIN CODES-----------------
class RestaurantStoreBinCodeSearchForm(forms.ModelForm):
    
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
        model = RestaurantStoreBinCode
        fields =['StoreBinCode','Description','CardNo']




class AddRestaurantStoreBinCodeForm(forms.ModelForm):
    class Meta:
        model = RestaurantStoreBinCode
        fields ='__all__'






#----------------EVENT CODE--------------------------
class RestaurantEventCodeSearchForm(forms.ModelForm):
    
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
        model = RestaurantEventCode
        fields =['Code','Description']



class AddRestaurantEventCodeForm(forms.ModelForm):
    class Meta:
        model = RestaurantEventCode
        fields ='__all__'






class RestaurantEventAlertSearchForm(forms.ModelForm):
    
    AlertID = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'AlertID', 'placeholder' : 'Enter AlertID'})

    )

    
    


    class Meta:
        model = RestaurantEventAlert
        fields =['AlertID']



class AddRestaurantEventAlertForm(forms.ModelForm):
    class Meta:
        model = RestaurantEventAlert
        fields ='__all__'









#-------------------Restaurant UOM------------------------------
class RestaurantUOMSearchForm(forms.ModelForm):
    
    UOMShortCode = forms.CharField(
        required=False,
    #label=False,
        widget=forms.TextInput(attrs={'id' :'UOMShortCode', 'placeholder' : 'Enter UOM Short Code'})

    )

        


    class Meta:
        model = RestaurantUOM
        fields =['UOMShortCode']




class AddRestaurantUOMForm(forms.ModelForm):
    class Meta:
        model = RestaurantUOM
        fields ='__all__'







#-------------------Restaurant BOM------------------------------
class RestaurantBOMSearchForm(forms.ModelForm):
    
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
        model = RestaurantBOM
        fields =['Code','Name']




class AddRestaurantBOMForm(forms.ModelForm):
    class Meta:
        model = RestaurantBOM
        fields ='__all__'



#----------UPLOAD BOM FILE-------------------
class AddRestaurantBOMFilesForm(forms.ModelForm):
    class Meta:
        model = RestaurantBOMFiles
        fields ='__all__'




#----------Restaurant  PRODUCTS CATEGORIES-------------------
class AddRestaurantCategoriesForm(forms.ModelForm):
    class Meta:
        model = RestaurantCategories
        fields ='__all__'



class AddRoomsClassesForm(forms.ModelForm):
    class Meta:
        model = RoomsClasses
        fields ='__all__'






















#-------------------Restaurant  PRODUCTS------------------------------
class RestaurantProductsSearchForm(forms.ModelForm):
    
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
        model = RestaurantProducts
        fields =['product_name','product_second_name','productCategory']



class AddRestaurantProductsForm(forms.ModelForm):
    class Meta:
        model = RestaurantProducts
        fields ='__all__'





































#-------------------------UPLOAD PRODUCTS-------------------

class UploadRestaurantProductsForm(forms.ModelForm):
    class Meta:
        model = RestaurantProducts
        fields ='__all__'
        








#------------------------Restaurant  SEARCH ORDERS---------------
# class RestaurantOrderSearchForm(forms.ModelForm):


         
#     class Meta:
#         model = RestaurantOrder
#         fields =['user']

class RestaurantOrderSearchForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'datepicker'}))

    end_date = forms.DateTimeField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'datepicker'}))

    export_to_CSV = forms.BooleanField(required=False)

    
         
    class Meta:
        model = RestaurantOrder
        fields =['user','start_date','end_date']
        #fields =['user']



















class RestaurantMyUserSearchForm(forms.ModelForm):
    
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









#-------------------Restaurant SUPPLIER MAINTENANCE--------------

class RestaurantSuppliersSearchForm(forms.ModelForm):
    
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
        model = RestaurantSuppliers
        fields =['SupplierFullName', 'Keyword','Status']



class AddRestaurantSuppliersForm(forms.ModelForm):
    class Meta:
        model = RestaurantSuppliers
        fields ='__all__'













#-----------------UNPAID Restaurant USERS--------------------

class UnpaidRestaurantMyUserSearchForm(forms.ModelForm):
    
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



#------------UPDATE UNPAID Restaurant USERS--------------
class UpdateUnpaidRestaurantMyUserForm(forms.ModelForm):
    
    class Meta:
        model = MyUser
        fields =['is_active','is_paid']






#-----------------PAID Restaurant USERS--------------------

class paidRestaurantMyUserSearchForm(forms.ModelForm):
    
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



#------------UPDATE UNPAID Restaurant USERS--------------
class UpdatepaidRestaurantMyUserForm(forms.ModelForm):
    
    class Meta:
        model = MyUser
        fields =['is_active','is_paid']

