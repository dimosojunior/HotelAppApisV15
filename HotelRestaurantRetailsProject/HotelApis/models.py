from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
import random
import string


# Create your models here.


#--------------MWANZO WA   HOTEL OTHER MODELS---------------------------------

class UserRole(models.Model):
    #id = models.CharField(max_length=100, primary_key=True)
    RoleName = models.CharField(verbose_name="Role Name", max_length=500,blank=False,null=False)
    
    def __str__(self):
        return self.RoleName
    
    class Meta:
        verbose_name_plural = "UserRole"

class VatRate(models.Model):
    #id = models.CharField(max_length=100, primary_key=True)
    RateName = models.CharField(verbose_name="Rate Name", max_length=500,blank=False,null=False)
    
    def __str__(self):
        return self.RateName
    
    class Meta:
        verbose_name_plural = "VatRate"

class AccountSystem(models.Model):
    #id = models.CharField(max_length=100, primary_key=True)
    AccountSystemName = models.CharField(verbose_name="Account System Name", max_length=500,blank=False,null=False)
    
    def __str__(self):
        return self.AccountSystemName
    
    class Meta:
        verbose_name_plural = "AccountSystem"


class GridDimensions(models.Model):
    #id = models.CharField(max_length=100, primary_key=True)
    GridDimensionsName = models.CharField(verbose_name="Grid Dimensions", max_length=500,blank=False,null=False)
    
    def __str__(self):
        return self.GridDimensionsName
    
    class Meta:
        verbose_name_plural = "GridDimensions"


class SigninTimeout(models.Model):
    #id = models.CharField(max_length=100, primary_key=True)
    SigninTimeoutName = models.CharField(verbose_name="Signin Timeout Name", max_length=500,blank=False,null=False)
    
    def __str__(self):
        return self.SigninTimeoutName
    
    class Meta:
        verbose_name_plural = "SigninTimeout"







class HotelBusinessUnit(models.Model):
    #id = models.CharField(max_length=100, primary_key=True)
    Code = models.CharField(verbose_name="Code", max_length=500,blank=False,null=False)
    Description = models.TextField(verbose_name="Description", max_length=1000,blank=True,null=True)
    status_Choices = (
            ('Active', 'Active'),
            ('Passive', 'Passive')
            )

    Status=models.CharField(verbose_name="Status",default="Active", choices=status_Choices, max_length=200, blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.Code + " " + self.Description
    
    class Meta:
        verbose_name_plural = "Hotel Business Unit"


class HotelLocationCode(models.Model):
    BusinessUnit = models.ForeignKey(HotelBusinessUnit,verbose_name="Business Unit", on_delete=models.PROTECT, blank=True,null=True)
    Code = models.CharField(verbose_name="Code", max_length=500,blank=False,null=False)
    Description = models.TextField(verbose_name="Description", max_length=1000,blank=True,null=True)
    status_Choices = (
            ('Active', 'Active'),
            ('Passive', 'Passive')
            )

    Status=models.CharField(verbose_name="Status",default="Active", choices=status_Choices, max_length=200, blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.Code + " " + self.Description
    
    class Meta:
        verbose_name_plural = "Hotel Location Code"







class HotelProcessConfig(models.Model):
    #BusinessUnit = models.ForeignKey(HotelBusinessUnit,verbose_name="Business Unit", on_delete=models.PROTECT, blank=True,null=True)
    ProcesId = models.CharField(verbose_name="Proces Id", max_length=500,blank=False,null=False)
    Description = models.TextField(verbose_name="Description", max_length=1000,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.ProcesId + " " +  self.Description
    
    class Meta:
        verbose_name_plural = "Hotel Process Config"




class HotelStoreCode(models.Model):
    Location = models.ForeignKey(HotelLocationCode,verbose_name="Store Location", on_delete=models.PROTECT, blank=True,null=True)
    Process = models.ForeignKey(HotelProcessConfig,verbose_name="Process", on_delete=models.PROTECT, blank=True,null=True)

    Code = models.CharField(verbose_name="Code", max_length=500,blank=False,null=False)
    Description = models.TextField(verbose_name="Description", max_length=1000,blank=True,null=True)
    status_Choices = (
            ('Active', 'Active'),
            ('Passive', 'Passive')
            )
    Status=models.CharField(verbose_name="Status",default="Active", choices=status_Choices, max_length=200, blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.Code + " " + self.Description
    
    class Meta:
        verbose_name_plural = "Hotel Store Code"



class HotelStoreBinCode(models.Model):
    #StoreCode = models.ForeignKey(HotelStoreCode,verbose_name="Store Code", on_delete=models.CASCADE, blank=True,null=True)
    StoreBinCode = models.CharField(verbose_name="Store Bin Code", max_length=500,blank=False,null=False)
    Description = models.TextField(verbose_name="Description", max_length=1000,blank=True,null=True)
    status_Choices = (
            ('Active', 'Active'),
            ('Passive', 'Passive')
            )

    Status=models.CharField(verbose_name="Status",default="Active", choices=status_Choices, max_length=200, blank=True,null=True)
    CardNo=models.CharField(verbose_name="Card No", max_length=200, blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.StoreBinCode + " " + self.Description
    
    class Meta:
        verbose_name_plural = "Hotel Store Bin Code"












class HotelEventCode(models.Model):
    Code = models.CharField(verbose_name="Code", max_length=500,blank=False,null=False)
    Description = models.TextField(verbose_name="Description", max_length=1000,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.Code + " " + self.Description
    
    class Meta:
        verbose_name_plural = "Hotel Event Code"

class HotelEventA(models.Model):
    EventDescription = models.TextField(verbose_name="Event Description", max_length=1000,blank=False,null=False)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.EventDescription
    
    class Meta:
        verbose_name_plural = "Hotel Event A"



class HotelEventB(models.Model):
    EventDescription = models.TextField(verbose_name="Event Description", max_length=1000,blank=False,null=False)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.EventDescription
    
    class Meta:
        verbose_name_plural = "Hotel Event B"

class HotelEventCategories(models.Model):
    CategoryName = models.CharField(verbose_name="Category Name", max_length=200,blank=False,null=False)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.CategoryName
    
    class Meta:
        verbose_name_plural = "Hotel Event Categories"

class HotelEventAlert(models.Model):
    EventA = models.ForeignKey(HotelEventA,verbose_name="Event A", on_delete=models.CASCADE, blank=True,null=True)
    EventB = models.ForeignKey(HotelEventB,verbose_name="Event B", on_delete=models.CASCADE, blank=True,null=True)
    Category = models.ForeignKey(HotelEventCategories,verbose_name="Category", on_delete=models.PROTECT, blank=True,null=True)

    AlertID = models.CharField(verbose_name="Code", max_length=500,blank=False,null=False)
    ReceivedBy = models.EmailField(verbose_name="Received By", max_length=1000,blank=True,null=True)
    PhoneNo = models.CharField(verbose_name="Phone No",default="+255", max_length=14,blank=True,null=True)
    Message = models.TextField(verbose_name="Message", max_length=1000,blank=True,null=True)
    status_Choices = (
            ('Active', 'Active'),
            ('Passive', 'Passive')
            )

    Status=models.CharField(verbose_name="Status",default="Active", choices=status_Choices, max_length=200, blank=True,null=True)

    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.AlertID + " " + self.ReceivedBy
    
    class Meta:
        verbose_name_plural = "Hotel Event Code"








class HotelUOM(models.Model):
    #StoreCode = models.ForeignKey(HotelStoreCode,verbose_name="Store Code", on_delete=models.CASCADE, blank=True,null=True)
    UOMShortCode = models.CharField(verbose_name="UOM Short Code", max_length=500,blank=False,null=False)
    Description = models.TextField(verbose_name="Description", max_length=1000,blank=True,null=True)
    status_Choices = (
            ('Active', 'Active'),
            ('Passive', 'Passive')
            )

    Status=models.CharField(verbose_name="Status",default="Active", choices=status_Choices, max_length=200, blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.UOMShortCode + " " + self.Description
    
    class Meta:
        verbose_name_plural = "Hotel UOM"



class HotelBOM(models.Model):
    #StoreCode = models.ForeignKey(HotelStoreCode,verbose_name="Store Code", on_delete=models.CASCADE, blank=True,null=True)
    Code = models.CharField(verbose_name="Code", max_length=500,blank=False,null=False)
    Name = models.CharField(verbose_name="Name", max_length=500,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.HotelBOM + " " + self.Name
    
    class Meta:
        verbose_name_plural = "Hotel BOM"


class HotelBOMFiles(models.Model):
    BOMCodeFile= models.FileField(verbose_name="BOM Code File", upload_to="media/BOMFiles", blank=False,null=False)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.BOMCodeFile 
    
    class Meta:
        verbose_name_plural = "Hotel BOM Files"






class HotelProductsUnit(models.Model):
    #StoreCode = models.ForeignKey(HotelStoreCode,verbose_name="Store Code", on_delete=models.CASCADE, blank=True,null=True)
    Unit = models.CharField(verbose_name="Unit", max_length=500,blank=True,null=True)
    Description = models.TextField(verbose_name="Description", max_length=500,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.Unit + " " + self.Description
    
    class Meta:
        verbose_name_plural = "Hotel Products Unit"












#----------------NEW PART 2--------------------------------
#-------------------HOTEL SUPPLIER---------------

class HotelSuppliers(models.Model):
    SupplierFullName = models.CharField(verbose_name="Supplier Full Name", max_length=500,blank=False,null=False)
    PhoneNumber = models.CharField(default="+255", verbose_name="Phone Number", max_length=14,blank=True,null=True)
    SupplierAddress = models.CharField(verbose_name="Supplier Address", max_length=200,blank=True,null=True)
    status_Choices = (
            ('Active', 'Active'),
            ('Passive', 'Passive')
            )

    Status=models.CharField(verbose_name="Status",default="Active", choices=status_Choices, max_length=200, blank=True,null=True)
    Keyword = models.CharField(verbose_name="Keyword", max_length=500,blank=True,null=True)

    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel Suppliers"
    
    def __str__(self):
        return self.SupplierFullName




#-----------------HOTEL TABLES----------------
class HotelTables(models.Model):
    TableNumber = models.CharField(verbose_name="Table Number",default="Table 20", max_length=500,blank=True,null=True)
    Description = models.TextField(verbose_name="Description", max_length=1000,blank=True,null=True)
    TableStatus = models.BooleanField(verbose_name="Table Status",default=False ,blank=True,null=True)
    
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel Tables"
    
    def __str__(self):
        return self.TableNumber









#--------------MWISHO WA   HOTEL OTHER MODELS---------------------------------

















class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("Your user name is required")
        
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            # phone=phone,
            # UserRole=UserRole,


            
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,

        )
        user.is_admin=True
        user.is_staff=True
        
        user.is_superuser=True

        user.is_hotel_user=True
        user.is_restaurant_user=True
        user.is_retails_user=True
        user.is_waiter=True
        user.is_supervisor=True
        is_paid=True

        user.save(using=self._db)
        return user

    

  
class MyUser(AbstractBaseUser):
    UserRole = models.ForeignKey(UserRole,verbose_name="User Role", on_delete=models.PROTECT,blank=True, null=True)
    email=models.EmailField(verbose_name="email", max_length=100, unique=True)
    first_name=models.CharField(verbose_name="first name", max_length=100, unique=False)
    username=models.CharField(verbose_name="user name", max_length=100, unique=True)
    middle_name=models.CharField(verbose_name="middle name", max_length=100, unique=False)
    last_name=models.CharField(verbose_name="last name", max_length=100, unique=False)
    company_name=models.CharField(verbose_name="company name", max_length=100, unique=False)
    phone=models.CharField(verbose_name="phone", max_length=15)
    UserCodes=models.CharField(verbose_name="User Codes", max_length=1000, unique=True, blank=True, null=True)
    profile_image = models.ImageField(upload_to='media/', blank=True, null=True)
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)

    AddressLine1=models.CharField(verbose_name="Address Line 1", max_length=500, blank=True, null=True)
    AddressLine2=models.CharField(verbose_name="Address Line 2", max_length=500, blank=True, null=True)
    VatNo=models.CharField(verbose_name="VAT No", max_length=500, blank=True, null=True)
    VatEnabled=models.BooleanField(verbose_name="VAT Enabled",default="True", blank=True, null=True)
    VatRate=models.ForeignKey(VatRate, verbose_name="VAT Rate",on_delete=models.PROTECT, blank=True, null=True)
    AccountSystem=models.ForeignKey(AccountSystem, verbose_name="Account System",on_delete=models.PROTECT, blank=True, null=True)
    ApprovedNeeded=models.BooleanField(verbose_name="Approved Needed",default="False", blank=True, null=True)


    #Terminal Configurations
    SigninTimeout=models.ForeignKey(SigninTimeout, verbose_name="Signin Timeout",on_delete=models.PROTECT, blank=True, null=True)
    PrintOrderItems=models.BooleanField(verbose_name="Print Order Items",default="True", blank=True, null=True)
    PrintConfirmedOrderSlip=models.BooleanField(verbose_name="Print Confirmed Order Slip",default="False", blank=True, null=True)
    GridDimensions=models.ForeignKey(GridDimensions, verbose_name="Grid Dimensions",on_delete=models.PROTECT, blank=True, null=True)


    #STOCK CONFIGURATIONS

    StockClosingTime=models.CharField(verbose_name="Stock Closing Time", max_length=1000, unique=False, blank=True, null=True)



    # Role_Choices = (
    #         ('MULTI TEACHER', 'MULTI TEACHER'),
    #         ('PHYSICS TEACHER', 'PHYSICS TEACHER'),
    #         ('CHEMISTRY TEACHER', 'CHEMISTRY TEACHER'),
    #         ('BIOLOGY TEACHER', 'BIOLOGY TEACHER'),
    #         ('ENGLISH TEACHER', 'ENGLISH TEACHER'),
    #         ('CIVICS TEACHER', 'CIVICS TEACHER'),
    #         ('MATHEMATICS TEACHER', 'MATHEMATICS TEACHER'),
    #         ('HISTORY TEACHER', 'HISTORY TEACHER'),
    #         ('GEOGRAPHY TEACHER', 'GEOGRAPHY TEACHER'),
    #         ('KISWAHILI TEACHER', 'KISWAHILI TEACHER'),
    #     )

    # role=models.CharField(verbose_name="role", choices=Role_Choices, max_length=50)
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_paid=models.BooleanField(default=False)

    is_hotel_user=models.BooleanField(default=False)
    is_restaurant_user=models.BooleanField(default=False)
    is_retails_user=models.BooleanField(default=False)

    is_waiter=models.BooleanField(default=False)
    is_supervisor=models.BooleanField(default=False)

    hide_email = models.BooleanField(default=True)
    


    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['username']
    
    objects=MyUserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Check if UserCode is not already set
        if not self.UserCodes:
            # Generate a unique random five-digit code
            while True:
                code = ''.join(random.choices(string.digits, k=8))
                if not MyUser.objects.filter(UserCodes=code).exists():
                    break

            self.UserCodes = code

        super(MyUser, self).save(*args, **kwargs)


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True



class HotelInventory(models.Model):

    Category = models.CharField(verbose_name="Category", max_length=100,blank=False,null=False)
    CategoryImage = models.ImageField(verbose_name="Category Image", upload_to='media/HotelInventoryImages/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel Inventory"

    def __str__(self):
        return self.Category









#-------------------HOTEL CUSTOMERS---------------

class HotelCustomers(models.Model):
    CustomerFullName = models.CharField(verbose_name="Customer Full Name", max_length=500,blank=False,null=False)
    PhoneNumber = models.CharField(default="+255", verbose_name="Phone Number", max_length=14,blank=True,null=True)
    CustomerAddress = models.CharField(verbose_name="Customer Address", max_length=200,blank=True,null=True)
    CustomerEmail = models.EmailField(verbose_name="Customer Email", max_length=200,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel Customers"
    
    def __str__(self):
        return self.CustomerFullName

#-------------------RESTAURANT CUSTOMERS---------------



















#----------------------- CATEGORY------------------

class HotelCategories(models.Model):
    Inventory = models.ForeignKey(HotelInventory,verbose_name="Category", on_delete=models.CASCADE, blank=True,null=True)
    Unit = models.ForeignKey(HotelProductsUnit,verbose_name="Product Unit", on_delete=models.PROTECT, blank=True,null=True)
    #ProductCategory = models.ForeignKey(HotelInventory, verbose_name="Product Category",on_delete=models.CASCADE, blank=True,null=True)

    CategoryName = models.CharField(verbose_name="Category Name", max_length=100,blank=False,null=False)
    Store = models.IntegerField(verbose_name="Quantity in Store",blank=True,null=True)
    CategoryImage = models.ImageField(verbose_name="Category Image", upload_to='media/Images/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel Categories"

    def __str__(self):
        return self.CategoryName




















#-----------------------ROOMS CATEGORIES------------------
class RoomsClasses(models.Model):
    Inventory = models.ForeignKey(HotelInventory,verbose_name="Category", on_delete=models.CASCADE, blank=True,null=True)
    Unit = models.ForeignKey(HotelProductsUnit,verbose_name="Unit", on_delete=models.PROTECT, blank=True,null=True)
    #ProductCategory = models.ForeignKey(HotelInventory, verbose_name="Product Category",on_delete=models.CASCADE, blank=True,null=True)

    RoomClass = models.CharField(verbose_name="Room Class", max_length=100,blank=False,null=False)
    Quantity = models.IntegerField(verbose_name="Quantity",blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Rooms Classes"

    def __str__(self):
        return self.RoomClass





#-----------------------PRODUCT UNIT------------------
# class ProductUnit(models.Model):

#     RoomClass = models.CharField(verbose_name="Room Class", max_length=100,blank=False,null=False)
#     Quantity = models.IntegerField(verbose_name="Quantity",blank=True,null=True)
#     Created = models.DateTimeField(auto_now_add=True)
#     Updated = models.DateTimeField(auto_now=True)

#     class Meta:
#         verbose_name_plural = "Product Unit"

#     def __str__(self):
#         return self.RoomClass








#----------------HOTEL PRODUCTS-------------------



#--------------------HOTEL  PRODUCTS-------------------


class HotelProducts(models.Model):
    StoreCode = models.ForeignKey(HotelStoreCode, verbose_name="Store Code",on_delete=models.CASCADE, blank=True,null=True)
    StoreBinCode = models.ForeignKey(HotelStoreBinCode, verbose_name="Store Bin Code",on_delete=models.PROTECT, blank=True,null=True)
    Unit = models.ForeignKey(HotelProductsUnit, verbose_name="Product Unit",on_delete=models.PROTECT, blank=True,null=True)

    product_name = models.CharField(default="Wali", verbose_name="Product Name", max_length=100,blank=False,null=False)
    product_second_name = models.CharField(default="",verbose_name="Product Second Name", max_length=100,blank=True,null=True)

    # Product_Category_Choices = (
    #     ('Pizza','Pizza'),
    #     ('Other ', 'Other '),
    #     )

    productCategory = models.ForeignKey(HotelCategories,verbose_name="Product Category",on_delete=models.CASCADE, blank=True,null=True)
    price = models.CharField(max_length=20,blank=True,null=True)
    #ProductUnit = models.CharField(verbose_name="Product Unit", max_length=100,blank=True,null=True)
    ProductQuantity = models.IntegerField(verbose_name="Product Quantity",blank=True,null=True)
    InitialProductQuantity = models.IntegerField(verbose_name="Initial Product Quantity",blank=True,null=True)
    CategoryImage = models.ImageField(verbose_name="Category Image", upload_to='media/HotelInventoryImages/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    
    
    class Meta:
        verbose_name_plural = "Hotel  Products"
        
    
    def __str__(self):
        #return f" {self.product_name} {self.product_second_name} "
        return f" {self.product_name} {self.product_second_name} "





class HotelCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(verbose_name="Total Price", default=0)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel  Cart"

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)
         


class HotelCartItems(models.Model):
    cart = models.ForeignKey(HotelCart, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(HotelProducts,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    #Customer = models.ForeignKey(HotelCustomers,on_delete=models.CASCADE,blank=True,null=True)

    # Customer = models.ForeignKey(HotelCustomers,on_delete=models.CASCADE,blank=True,null=True)

    # table = models.ForeignKey(HotelTables,on_delete=models.PROTECT,blank=True,null=True)
    # room = models.ForeignKey('HotelRooms',on_delete=models.PROTECT,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel  Cart Items"
    
    def __str__(self):
        return f" {self.product.product_name} {self.product.product_second_name} "
        
    

@receiver(pre_save, sender=HotelCartItems)
def hotel__correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = HotelProducts.objects.get(id=cart_items.product.id)
    cart_items.price = cart_items.quantity * float(price_of_product.price)
    # total_cart_items = CartItems.objects.filter(user = cart_items.user )
    # cart = Cart.objects.get(id = cart_items.cart.id)
    # cart.total_price = cart_items.price
    # cart.save()



class HotelOrder(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    cart = models.ForeignKey(HotelCart, on_delete=models.CASCADE, blank=True, null=True)
    #orderItems = models.ManyToManyField('HotelOrderItems', blank=True,null=True)
    total_price = models.FloatField(verbose_name="Total Price")

    CategoryId = models.IntegerField(verbose_name="Category ID",blank=True,null=True)
    
    table_number = models.CharField(max_length=500, verbose_name="Table Number",blank=True,null=True)
    
    room_number = models.CharField(max_length=500, verbose_name="Room Number",blank=True,null=True)
    number_of_days = models.IntegerField(verbose_name="Number of days",blank=True,null=True)
    room_price = models.FloatField(verbose_name="Room Price",blank=True,null=True)

    pending_total_price = models.FloatField(verbose_name="Pending Total Price",blank=True,null=True)
    true_total_price = models.FloatField(verbose_name="True Total Price",blank=True,null=True)

    order_status = models.BooleanField(verbose_name="Status", default=False,blank=True,null=True)
    closed_order_state = models.BooleanField(verbose_name="Is Order Closed ?", default=False,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    #items = models.ForeignKey('HotelOrderItems', on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Hotel  Orders"
        #db_table='HotelOrderTable'

    

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class HotelOrderItems(models.Model):
    order = models.ForeignKey(HotelOrder, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    product = models.ForeignKey(HotelProducts,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    Customer = models.ForeignKey(HotelCustomers,on_delete=models.CASCADE,blank=True,null=True)
    table = models.ForeignKey(HotelTables,on_delete=models.PROTECT,blank=True,null=True)
    room = models.ForeignKey('HotelRooms',on_delete=models.PROTECT,blank=True,null=True)
    order_status = models.BooleanField(verbose_name="Status", default=False,blank=True,null=True)


    quantity = models.IntegerField(default=1)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel  Orders Items"

    def __str__(self):
        #return f" {self.product.product_name} {self.product.product_second_name} "
        return f" {self.product.product_name} {self.product.product_second_name} "













































        #-----------------------ROOMS------------------

#--------------------HOTEL ROOMS -------------------


class HotelRooms(models.Model):
    RoomName = models.CharField(default="Room 1", verbose_name="Room Name", max_length=100,blank=False,null=False)
    RoomClass = models.ForeignKey(RoomsClasses, on_delete=models.CASCADE,verbose_name="Room Class", max_length=100,blank=True,null=True)
    Unit = models.ForeignKey(HotelProductsUnit, verbose_name="Product Unit",on_delete=models.PROTECT, blank=True,null=True)

    price = models.CharField(max_length=50,blank=True,null=True)
    RoomFloor = models.CharField(verbose_name="Room Floor", max_length=100,blank=True,null=True)
    RoomStatus = models.BooleanField(verbose_name="Room Status",default=False, max_length=100,blank=True,null=True)
    ProductQuantity = models.IntegerField(default=1, verbose_name="Quantity",blank=True,null=True)
    InitialProductQuantity = models.IntegerField(default=1, verbose_name="Initial Quantity",blank=True,null=True)
    RoomImage = models.ImageField(verbose_name="Room Image", upload_to='media/RoomImages/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    
    
    class Meta:
        verbose_name_plural = "Hotel Rooms"
        
    
    def __str__(self):
        return self.RoomName





class HotelRoomsCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(verbose_name="Total Price", default=0)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel Rooms Cart"

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)
         


class HotelRoomsCartItems(models.Model):
    cart = models.ForeignKey(HotelRoomsCart, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(HotelRooms,on_delete=models.CASCADE)
    #table = models.ForeignKey(HotelTables,on_delete=models.PROTECT,blank=True,null=True)
    price = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    #Customer = models.ForeignKey(HotelCustomers,on_delete=models.CASCADE,blank=True,null=True)
    DaysNumber = models.IntegerField(verbose_name="Number of Days",blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel Rooms Cart Items"
    
    def __str__(self):
        return str(self.user.username) + " " + str(self.room.RoomName)
        
    

@receiver(pre_save, sender=HotelRoomsCartItems)
def hotel_Rooms_correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_room = HotelRooms.objects.get(id=cart_items.room.id)
    cart_items.price = cart_items.DaysNumber * float(price_of_room.price)
    # total_cart_items = CartItems.objects.filter(user = cart_items.user )
    # cart = Cart.objects.get(id = cart_items.cart.id)
    # cart.total_price = cart_items.price
    # cart.save()



class HotelRoomsOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    cart = models.ForeignKey(HotelRoomsCart, on_delete=models.CASCADE, blank=True, null=True)
    #orderItems = models.ManyToManyField('HotelRoomsOrderItems')
    total_price = models.FloatField(verbose_name="Total Price")
    closed_order_state = models.BooleanField(verbose_name="Is Order Closed ?", default=False,blank=True,null=True)

    
    #room_number = models.CharField(max_length=500, verbose_name="Room Number",blank=True,null=True)

    
    order_status = models.BooleanField(verbose_name="Status", default=False,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    items = models.ForeignKey('HotelRoomsOrderItems', on_delete=models.CASCADE,blank=True, null=True)

    class Meta:
        verbose_name_plural = "Hotel Rooms Orders"

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class HotelRoomsOrderItems(models.Model):
    order = models.ForeignKey(HotelRoomsOrder, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(HotelRooms,on_delete=models.CASCADE)
    table = models.ForeignKey(HotelTables,on_delete=models.PROTECT,blank=True,null=True)
    price = models.FloatField(default=0)
    order_status = models.BooleanField(verbose_name="Status", default=False,blank=True,null=True)
    quantity = models.IntegerField(default=1)

    is_customer_opened_closed = models.BooleanField(verbose_name="Customer Opened/Closed Status", default=False,blank=True,null=True)
    
    
    Customer = models.ForeignKey(HotelCustomers,on_delete=models.CASCADE,blank=True,null=True)
    DaysNumber = models.IntegerField(verbose_name="Number of Days",blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Hotel Rooms Orders Items"

    def __str__(self):
        return str(self.user.username) + " " + str(self.room.RoomName)













