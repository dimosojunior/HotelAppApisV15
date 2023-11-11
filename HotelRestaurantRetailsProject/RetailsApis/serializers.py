from rest_framework.validators import UniqueValidator
#from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
#from django.contrib.auth.models import User
from HotelApis.models import *
from .models import *




#--------------------------------------------------------------

from rest_framework import serializers
#from django.contrib.auth.models import User

class RetailsTablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsTables
        fields = '__all__'


class RetailsInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsInventory
        fields = '__all__'


#------------------PRODUCTS UNIT----------------------------



class RetailsProductsUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsProductsUnit
        fields = '__all__'


class RetailsCategoriesSerializer(serializers.ModelSerializer):
    Unit = RetailsProductsUnitSerializer(many=False)
    class Meta:
        model = RetailsCategories
        fields = '__all__'





class RetailsCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsCustomers
        fields = '__all__'










#HIZI NI KWAAJILI YA KUADD PRODUCTS KWASABABU TUKITUMIA HIZO ZA CHINI
#BILA KUTOA HIYO Unit FIELD INALETA ERROR SO  ILI KUAVOID HIYO ERROR
#TUNATUMIA HIZI KWAAJILI YA KUADD PRODUCT

class AddRetailsProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsProducts
        fields = '__all__'




#MWISHO WA HIZO ZA KUADD PRODUCTS


#-----------------Retails  PRODUCTS------------------
class RetailsProductsSerializer(serializers.ModelSerializer):
    Unit = RetailsProductsUnitSerializer(many=False)
    class Meta:
        model = RetailsProducts
        fields = '__all__'









#---------------------Retails  CART SERIALIZER---------


class RetailsCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsCart
        fields = '__all__'


class RetailsCartItemsSerializer(serializers.ModelSerializer):
    cart = RetailsCartSerializer()
    product = RetailsProductsSerializer()

    #table = RetailsTablesSerializer()
    class Meta:
        model = RetailsCartItems
        fields = '__all__'



class RetailsOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailsOrder
        fields = '__all__'


class RetailsOrderItemsSerializer(serializers.ModelSerializer):
    order = RetailsOrderSerializer()
    product = RetailsProductsSerializer()

    table = RetailsTablesSerializer()
    Customer = RetailsCustomersSerializer()
    class Meta:
        model = RetailsOrderItems
        fields = '__all__'













#-----------GET HOTEL WAITERS----------------
class RetailsWaitersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'







