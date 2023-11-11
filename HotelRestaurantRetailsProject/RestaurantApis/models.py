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
from HotelApis.models import *






# HII MODELS INABEBA PRODUCTS TU NA CART FUNCTIONALITIES







#--------------MWANZO WA   Restaurant OTHER MODELS---------------------------------

# class RestaurantUserRole(models.Model):
#     #id = models.CharField(max_length=100, primary_key=True)
#     RoleName = models.CharField(verbose_name="Role Name", max_length=500,blank=False,null=False)
    
#     def __str__(self):
#         return self.RoleName
    
#     class Meta:
#         verbose_name_plural = "UserRole"

class RestaurantVatRate(models.Model):
    #id = models.CharField(max_length=100, primary_key=True)
    RateName = models.CharField(verbose_name="Rate Name", max_length=500,blank=False,null=False)
    
    def __str__(self):
        return self.RateName
    
    class Meta:
        verbose_name_plural = "VatRate"

class RestaurantAccountSystem(models.Model):
    #id = models.CharField(max_length=100, primary_key=True)
    AccountSystemName = models.CharField(verbose_name="Account System Name", max_length=500,blank=False,null=False)
    
    def __str__(self):
        return self.AccountSystemName
    
    class Meta:
        verbose_name_plural = "AccountSystem"


class RestaurantGridDimensions(models.Model):
    #id = models.CharField(max_length=100, primary_key=True)
    GridDimensionsName = models.CharField(verbose_name="Grid Dimensions", max_length=500,blank=False,null=False)
    
    def __str__(self):
        return self.GridDimensionsName
    
    class Meta:
        verbose_name_plural = "GridDimensions"


class RestaurantSigninTimeout(models.Model):
    #id = models.CharField(max_length=100, primary_key=True)
    SigninTimeoutName = models.CharField(verbose_name="Signin Timeout Name", max_length=500,blank=False,null=False)
    
    def __str__(self):
        return self.SigninTimeoutName
    
    class Meta:
        verbose_name_plural = "SigninTimeout"







class RestaurantBusinessUnit(models.Model):
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
        verbose_name_plural = "Restaurant Business Unit"


class RestaurantLocationCode(models.Model):
    BusinessUnit = models.ForeignKey(RestaurantBusinessUnit,verbose_name="Business Unit", on_delete=models.PROTECT, blank=True,null=True)
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
        verbose_name_plural = "Restaurant Location Code"







class RestaurantProcessConfig(models.Model):
    #BusinessUnit = models.ForeignKey(RestaurantBusinessUnit,verbose_name="Business Unit", on_delete=models.PROTECT, blank=True,null=True)
    ProcesId = models.CharField(verbose_name="Proces Id", max_length=500,blank=False,null=False)
    Description = models.TextField(verbose_name="Description", max_length=1000,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.ProcesId + " " +  self.Description
    
    class Meta:
        verbose_name_plural = "Restaurant Process Config"




class RestaurantStoreCode(models.Model):
    Location = models.ForeignKey(RestaurantLocationCode,verbose_name="Store Location", on_delete=models.PROTECT, blank=True,null=True)
    Process = models.ForeignKey(RestaurantProcessConfig,verbose_name="Process", on_delete=models.PROTECT, blank=True,null=True)

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
        verbose_name_plural = "Restaurant Store Code"



class RestaurantStoreBinCode(models.Model):
    #StoreCode = models.ForeignKey(RestaurantStoreCode,verbose_name="Store Code", on_delete=models.CASCADE, blank=True,null=True)
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
        verbose_name_plural = "Restaurant Store Bin Code"












class RestaurantEventCode(models.Model):
    Code = models.CharField(verbose_name="Code", max_length=500,blank=False,null=False)
    Description = models.TextField(verbose_name="Description", max_length=1000,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.Code + " " + self.Description
    
    class Meta:
        verbose_name_plural = "Restaurant Event Code"

class RestaurantEventA(models.Model):
    EventDescription = models.TextField(verbose_name="Event Description", max_length=1000,blank=False,null=False)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.EventDescription
    
    class Meta:
        verbose_name_plural = "Restaurant Event A"



class RestaurantEventB(models.Model):
    EventDescription = models.TextField(verbose_name="Event Description", max_length=1000,blank=False,null=False)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.EventDescription
    
    class Meta:
        verbose_name_plural = "Restaurant Event B"

class RestaurantEventCategories(models.Model):
    CategoryName = models.CharField(verbose_name="Category Name", max_length=200,blank=False,null=False)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.CategoryName
    
    class Meta:
        verbose_name_plural = "Restaurant Event Categories"

class RestaurantEventAlert(models.Model):
    EventA = models.ForeignKey(RestaurantEventA,verbose_name="Event A", on_delete=models.CASCADE, blank=True,null=True)
    EventB = models.ForeignKey(RestaurantEventB,verbose_name="Event B", on_delete=models.CASCADE, blank=True,null=True)
    Category = models.ForeignKey(RestaurantEventCategories,verbose_name="Category", on_delete=models.PROTECT, blank=True,null=True)

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
        verbose_name_plural = "Restaurant Event Code"








class RestaurantUOM(models.Model):
    #StoreCode = models.ForeignKey(RestaurantStoreCode,verbose_name="Store Code", on_delete=models.CASCADE, blank=True,null=True)
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
        verbose_name_plural = "Restaurant UOM"



class RestaurantBOM(models.Model):
    #StoreCode = models.ForeignKey(RestaurantStoreCode,verbose_name="Store Code", on_delete=models.CASCADE, blank=True,null=True)
    Code = models.CharField(verbose_name="Code", max_length=500,blank=False,null=False)
    Name = models.CharField(verbose_name="Name", max_length=500,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.RestaurantBOM + " " + self.Name
    
    class Meta:
        verbose_name_plural = "Restaurant BOM"


class RestaurantBOMFiles(models.Model):
    BOMCodeFile= models.FileField(verbose_name="BOM Code File", upload_to="media/BOMFiles", blank=False,null=False)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.BOMCodeFile 
    
    class Meta:
        verbose_name_plural = "Restaurant BOM Files"




class RestaurantProductsUnit(models.Model):
    #StoreCode = models.ForeignKey(RestaurantStoreCode,verbose_name="Store Code", on_delete=models.CASCADE, blank=True,null=True)
    Unit = models.CharField(verbose_name="Unit", max_length=500,blank=False,null=False)
    Description = models.TextField(verbose_name="Description", max_length=500,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.Unit + " " + self.Description
    
    class Meta:
        verbose_name_plural = "Restaurant Products Unit"






class RestaurantSuppliers(models.Model):
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
        verbose_name_plural = "Restaurant Suppliers"
    
    def __str__(self):
        return self.SupplierFullName







class RestaurantTables(models.Model):
    TableNumber = models.CharField(verbose_name="Table Number",default="Table 20", max_length=500,blank=True,null=True)
    Description = models.TextField(verbose_name="Description", max_length=1000,blank=True,null=True)
    TableStatus = models.BooleanField(verbose_name="Table Status",default=False ,blank=True,null=True)
    
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Restaurant Tables"
    
    def __str__(self):
        return self.TableNumber



#--------------MWISHO WA   Restaurant OTHER MODELS---------------------------------



class RestaurantInventory(models.Model):

    Category = models.CharField(verbose_name="Category", max_length=100,blank=False,null=False)
    CategoryImage = models.ImageField(verbose_name="Category Image", upload_to='media/RestaurantInventoryImages/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Restaurant Inventory"

    def __str__(self):
        return self.Category




class RestaurantCategories(models.Model):
    Inventory = models.ForeignKey(HotelInventory,verbose_name="Category", on_delete=models.CASCADE, blank=True,null=True)
    Unit = models.ForeignKey(RestaurantProductsUnit,verbose_name="Product Unit", on_delete=models.PROTECT, blank=True,null=True)
    #ProductCategory = models.ForeignKey(RestaurantInventory, verbose_name="Product Category",on_delete=models.CASCADE, blank=True,null=True)

    CategoryName = models.CharField(verbose_name="Category Name", max_length=100,blank=False,null=False)
    Store = models.IntegerField(verbose_name="Quantity in Store",blank=True,null=True)
    CategoryImage = models.ImageField(verbose_name="Category Image", upload_to='media/Images/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Restaurant Categories"

    def __str__(self):
        return self.CategoryName







class RestaurantCustomers(models.Model):
    CustomerFullName = models.CharField(verbose_name="Customer Full Name", max_length=500,blank=False,null=False)
    PhoneNumber = models.CharField(default="+255", verbose_name="Phone Number", max_length=14,blank=True,null=True)
    CustomerAddress = models.CharField(verbose_name="Customer Address", max_length=200,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Restaurant Customers"
    
    def __str__(self):
        return self.CustomerFullName














#----------------Restaurant PRODUCTS-------------------



#--------------------Restaurant  PRODUCTS-------------------


class RestaurantProducts(models.Model):
    StoreCode = models.ForeignKey(RestaurantStoreCode, verbose_name="Store Code",on_delete=models.CASCADE, blank=True,null=True)
    StoreBinCode = models.ForeignKey(RestaurantStoreBinCode, verbose_name="Store Bin Code",on_delete=models.PROTECT, blank=True,null=True)
    Unit = models.ForeignKey(RestaurantProductsUnit, verbose_name="Product Unit",on_delete=models.PROTECT, blank=True,null=True)

    product_name = models.CharField(default="Wali", verbose_name="Product Name", max_length=100,blank=False,null=False)
    product_second_name = models.CharField(default="",verbose_name="Product Second Name", max_length=100,blank=True,null=True)

    # Product_Category_Choices = (
    #     ('Pizza','Pizza'),
    #     ('Other ', 'Other '),
    #     )

    productCategory = models.ForeignKey(RestaurantCategories,verbose_name="Product Category",on_delete=models.CASCADE, blank=True,null=True)
    price = models.CharField(max_length=20,blank=True,null=True)
    #ProductUnit = models.CharField(verbose_name="Product Unit", max_length=100,blank=True,null=True)
    ProductQuantity = models.IntegerField(verbose_name="Product Quantity",blank=True,null=True)
    InitialProductQuantity = models.IntegerField(verbose_name="Initial Product Quantity",blank=True,null=True)
    CategoryImage = models.ImageField(verbose_name="Category Image", upload_to='media/RestaurantInventoryImages/',blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    
    
    class Meta:
        verbose_name_plural = "Restaurant  Products"
        
    
    def __str__(self):
        return f" {self.product_name} {self.product_second_name} "





class RestaurantCart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    total_price = models.FloatField(verbose_name="Total Price", default=0)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Restaurant  Cart"

    def __str__(self):
        return str(self.user.username) + " " + str(self.total_price)
         


class RestaurantCartItems(models.Model):
    cart = models.ForeignKey(RestaurantCart, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(RestaurantProducts,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    #Customer = models.ForeignKey(RestaurantCustomers,on_delete=models.CASCADE,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    #table = models.ForeignKey(RestaurantTables,on_delete=models.PROTECT,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Restaurant  Cart Items"
    
    def __str__(self):
        return f" {self.product.product_name} {self.product.product_second_name} "
        
    

@receiver(pre_save, sender=RestaurantCartItems)
def Restaurant__correct_price(sender, **kwargs):
    cart_items = kwargs['instance']
    price_of_product = RestaurantProducts.objects.get(id=cart_items.product.id)
    cart_items.price = cart_items.quantity * float(price_of_product.price)
    # total_cart_items = CartItems.objects.filter(user = cart_items.user )
    # cart = Cart.objects.get(id = cart_items.cart.id)
    # cart.total_price = cart_items.price
    # cart.save()



class RestaurantOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    cart = models.ForeignKey(RestaurantCart, on_delete=models.CASCADE, blank=True, null=True)
    orderItems = models.ManyToManyField('RestaurantOrderItems')
    total_price = models.FloatField(verbose_name="Total Price")

    CategoryId = models.IntegerField(verbose_name="Category ID",blank=True,null=True)
    closed_order_state = models.BooleanField(verbose_name="Is Order Closed ?", default=False,blank=True,null=True)

    table_number = models.CharField(max_length=500, verbose_name="Table Number",blank=True,null=True)

    order_status = models.BooleanField(verbose_name="Status", default=False,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Restaurant Orders"

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class RestaurantOrderItems(models.Model):
    order = models.ForeignKey(RestaurantOrder, on_delete=models.CASCADE) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(RestaurantProducts,on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    Customer = models.ForeignKey(RestaurantCustomers,on_delete=models.CASCADE,blank=True,null=True)
    order_status = models.BooleanField(verbose_name="Status", default=False,blank=True,null=True)
    quantity = models.IntegerField(default=1)
    table = models.ForeignKey(RestaurantTables,on_delete=models.PROTECT,blank=True,null=True)
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Restaurant Orders Items"

    def __str__(self):
        return f" {self.product.product_name} {self.product.product_second_name} " 































