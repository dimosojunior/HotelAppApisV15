from rest_framework.validators import UniqueValidator
#from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
#from django.contrib.auth.models import User
from .models import *




#--------------------------------------------------------------

from rest_framework import serializers
#from django.contrib.auth.models import User
class HotelBusinessUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelBusinessUnit
        fields = '__all__'


class HotelLocationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelLocationCode
        fields = '__all__'





class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

class HotelTablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelTables
        fields = '__all__'



        
class HotelInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelInventory
        fields = '__all__'

class HotelProductsUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelProductsUnit
        fields = '__all__'


class HotelCategoriesSerializer(serializers.ModelSerializer):
    Unit = HotelProductsUnitSerializer(many=False)
    class Meta:
        model = HotelCategories
        fields = '__all__'





class RoomsClassesSerializer(serializers.ModelSerializer):
    Unit = HotelProductsUnitSerializer(many=False)
    class Meta:
        model = RoomsClasses
        fields = '__all__'



class HotelCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelCustomers
        fields = '__all__'


#------------------PRODUCTS UNIT----------------------------






#HIZI NI KWAAJILI YA KUADD PRODUCTS KWASABABU TUKITUMIA HIZO ZA CHINI
#BILA KUTOA HIYO Unit FIELD INALETA ERROR SO  ILI KUAVOID HIYO ERROR
#TUNATUMIA HIZI KWAAJILI YA KUADD PRODUCT

class AddHotelProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelProducts
        fields = '__all__'



class AddHotelRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRooms
        fields = '__all__'

#MWISHO WA HIZO ZA KUADD PRODUCTS


#-----------------HOTEL  PRODUCTS------------------
class HotelProductsSerializer(serializers.ModelSerializer):
    Unit = HotelProductsUnitSerializer(many=False)  # Set many=False for the foreign key relationship
    class Meta:
        model = HotelProducts
        fields = '__all__'




#-----------------HOTEL ROOMS PRODUCTS------------------
class HotelRoomsSerializer(serializers.ModelSerializer):
    Unit = HotelProductsUnitSerializer(many=False)
    class Meta:
        model = HotelRooms
        fields = '__all__'








#---------------------HOTEL  CART SERIALIZER---------


class HotelCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelCart
        fields = '__all__'


class HotelCartItemsSerializer(serializers.ModelSerializer):
    cart = HotelCartSerializer()
    product = HotelProductsSerializer()

    # table = HotelTablesSerializer()
    # room = HotelRoomsSerializer()
    class Meta:
        model = HotelCartItems
        fields = '__all__'



class HotelOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelOrder
        fields = '__all__'


class HotelOrderItemsSerializer(serializers.ModelSerializer):
    order = HotelOrderSerializer()
    product = HotelProductsSerializer()

    table = HotelTablesSerializer()
    room = HotelRoomsSerializer()
    Customer = HotelCustomersSerializer()
    class Meta:
        model = HotelOrderItems
        fields = '__all__'


















#---------------------HOTEL ROOMS CART SERIALIZER---------


class HotelRoomsCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoomsCart
        fields = '__all__'


class HotelRoomsCartItemsSerializer(serializers.ModelSerializer):
    cart = HotelRoomsCartSerializer()
    room = HotelRoomsSerializer()
    # Customer = HotelCustomers()
    class Meta:
        model = HotelRoomsCartItems
        fields = '__all__'



class HotelRoomsOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelRoomsOrder
        fields = '__all__'


class HotelRoomsOrderItemsSerializer(serializers.ModelSerializer):
    order = HotelRoomsOrderSerializer()
    room = HotelRoomsSerializer()
    Customer = HotelCustomersSerializer()
    class Meta:
        model = HotelRoomsOrderItems
        fields = '__all__'













#-----------GET HOTEL WAITERS----------------
class HotelWaitersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'










