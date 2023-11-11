from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin





from import_export.admin import ImportExportModelAdmin

# @admin.register(UserRole) 

# class ViewAdmin(ImportExportModelAdmin):
#     pass





class MyUserAdmin(BaseUserAdmin):
    list_display=('id','username', 'email','UserRole','company_name', 'date_joined', 'last_login', 'is_admin', 'is_active', 'is_hotel_user','is_restaurant_user','is_retails_user')
    search_fields=('email', 'first_name', 'last_name')
    readonly_fields=('date_joined', 'last_login')
    filter_horizontal=()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None,{
            'classes':('wide'),
            'fields':('email', 'username', 'password1', 'password2','phone','UserRole'),
        }),
    )

    ordering=('email',)



#----------------INVENTORIES------------
class HotelInventoryAdmin(admin.ModelAdmin):

    list_display = ["id", "Category","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Category"]















#------------------CUSTOMERS---------------------------

class HotelCustomersAdmin(admin.ModelAdmin):

    list_display = ["id", "CustomerFullName","PhoneNumber","CustomerAddress","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CustomerFullName"]








#----------------------- CATEGORY--------------------


class HotelCategoriesAdmin(admin.ModelAdmin):

    list_display = ["id","Inventory", "CategoryName","Store","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["CategoryName"]



















#-----------------------ROOM CLASSES----------------------------------

class RoomsClassesAdmin(admin.ModelAdmin):

    list_display = ["id","RoomClass","Quantity","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["RoomClass"]











#--------------------------Hotel  ProductsS--------------------

@admin.register(HotelProducts)
class HotelProductsAdmin(ImportExportModelAdmin):

    list_display = ["id","product_name","product_second_name","productCategory", "price","ProductQuantity","Created","Updated"]
    list_filter =["Created","Updated","productCategory"]
    search_fields = ["product_name","product_second_name"]





#--------------------------Hotel ROOMS ProductsS--------------------

@admin.register(HotelRooms)
class HotelRoomsAdmin(ImportExportModelAdmin):

    list_display = ["id","RoomName","RoomClass","RoomFloor","RoomStatus","price","Created","Updated"]
    list_filter =["RoomStatus", "Created","Updated","RoomClass"]
    search_fields = ["RoomName"]










#---------------------HOTEL  CART---------------------
class HotelCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class HotelCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","user","cart", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]

@admin.register(HotelOrder)    
class HotelOrderAdmin(ImportExportModelAdmin):
    list_display = ["id","user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

@admin.register(HotelOrderItems) 
class HotelOrderItemsAdmin(ImportExportModelAdmin):
    list_display = ["id","user","order", "product","price","quantity", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]












#---------------------HOTEL ROOMS CART---------------------
class HotelRoomsCartAdmin(admin.ModelAdmin):
    list_display = ["id","user","ordered", "total_price", "Created","Updated"]
    list_filter =["Created"]
    search_fields = ["user"]

class HotelRoomsCartItemsAdmin(admin.ModelAdmin):
    list_display = ["id","room","DaysNumber","price", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]

@admin.register(HotelRoomsOrder)   
class HotelRoomsOrderAdmin(ImportExportModelAdmin):
    list_display = ["user","total_price", "created"]
    list_filter =["created"]
    search_fields = ["user"]

@admin.register(HotelRoomsOrderItems)
class HotelRoomsOrderItemsAdmin(ImportExportModelAdmin):
    list_display = ["id","Customer","DaysNumber", "room","price", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["user"]











class HotelLocationCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","BusinessUnit","Status", "Created","Updated"]
    list_filter =["BusinessUnit", "Created","Updated"]
    search_fields = ["Code"]

class HotelBusinessUnitAdmin(admin.ModelAdmin):
    list_display = ["Code","Status", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code"]

class HotelProcessConfigAdmin(admin.ModelAdmin):
    list_display = ["ProcesId","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["ProcesId"]

class HotelStoreCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","Location","Process","Description","Status", "Created","Updated"]
    list_filter =["Location","Process","Status"]
    search_fields = ["Code"]

class HotelStoreBinCodeAdmin(admin.ModelAdmin):
    list_display = ["StoreBinCode","CardNo", "Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["StoreBinCode"]



class HotelEventCodeAdmin(admin.ModelAdmin):
    list_display = ["Code","Description","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code"]


class HotelEventAlertAdmin(admin.ModelAdmin):
    list_display = ["AlertID","ReceivedBy","PhoneNo","EventA","EventB","Category", "Created","Updated"]
    list_filter =["Category","EventA", "EventB", "Created","Updated"]
    search_fields = ["AlertID","ReceivedBy"]



class HotelUOMAdmin(admin.ModelAdmin):
    list_display = ["UOMShortCode", "Status","Description","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["UOMShortCode"]

class HotelBOMAdmin(admin.ModelAdmin):
    list_display = ["Code", "Name","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Code", "Name"]

class HotelBOMFilesAdmin(admin.ModelAdmin):
    list_display = ["BOMCodeFile","Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["BOMCodeFile"]





class HotelProductsUnitAdmin(admin.ModelAdmin):

    list_display = ["id", "Unit","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["Unit"]



class HotelSuppliersAdmin(admin.ModelAdmin):

    list_display = ["SupplierFullName","PhoneNumber","SupplierAddress","Status", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["SupplierFullName"]


class HotelTablesAdmin(admin.ModelAdmin):

    list_display = ["TableNumber","Description", "Created","Updated"]
    list_filter =["Created","Updated"]
    search_fields = ["TableNumber"]
#-----------------MWISHO WA OTHER MODELS------------------

admin.site.register(MyUser, MyUserAdmin)




#-----------------MWANZO WA OTHER MODELS------------------
admin.site.register(UserRole)
admin.site.register(VatRate)
admin.site.register(AccountSystem)
admin.site.register(GridDimensions)
admin.site.register(SigninTimeout)
admin.site.register(HotelEventA)
admin.site.register(HotelEventB)
admin.site.register(HotelEventCategories)


admin.site.register(HotelStoreBinCode, HotelStoreBinCodeAdmin)
admin.site.register(HotelStoreCode, HotelStoreCodeAdmin)
admin.site.register(HotelProcessConfig, HotelProcessConfigAdmin)
admin.site.register(HotelEventCode, HotelEventCodeAdmin)
admin.site.register(HotelEventAlert, HotelEventAlertAdmin)
admin.site.register(HotelUOM, HotelUOMAdmin)
admin.site.register(HotelBOM, HotelBOMAdmin)
admin.site.register(HotelBOMFiles, HotelBOMFilesAdmin)
admin.site.register(HotelProductsUnit, HotelProductsUnitAdmin)
admin.site.register(HotelSuppliers, HotelSuppliersAdmin)

admin.site.register(HotelTables, HotelTablesAdmin)




#-----------------MWISHO WA OTHER MODELS------------------

admin.site.register(HotelInventory, HotelInventoryAdmin)




#--------------------CUSTOMERS-----------------
admin.site.register(HotelCustomers, HotelCustomersAdmin)



#---------------- CATEGORY-----------------

admin.site.register(HotelCategories, HotelCategoriesAdmin)





#----------------ROOM CLASSES----------------
admin.site.register(RoomsClasses, RoomsClassesAdmin)


#---------------------HOTEL  PRODUCTS--------------------
#admin.site.register(HotelProducts, HotelProductsAdmin)
admin.site.register(HotelCart, HotelCartAdmin)
admin.site.register(HotelCartItems, HotelCartItemsAdmin)
#admin.site.register(HotelOrder,HotelOrderAdmin)
#admin.site.register(HotelOrderItems,HotelOrderItemsAdmin)







#---------------------HOTEL ROOMS --------------------
#admin.site.register(HotelRooms, HotelRoomsAdmin)
admin.site.register(HotelRoomsCart, HotelRoomsCartAdmin)
admin.site.register(HotelRoomsCartItems, HotelRoomsCartItemsAdmin)
#admin.site.register(HotelRoomsOrder,HotelRoomsOrderAdmin)
#admin.site.register(HotelRoomsOrderItems,HotelRoomsOrderItemsAdmin)















#--------------------------OTHER MODELS-----------------

admin.site.register(HotelBusinessUnit, HotelBusinessUnitAdmin)
admin.site.register(HotelLocationCode, HotelLocationCodeAdmin)













