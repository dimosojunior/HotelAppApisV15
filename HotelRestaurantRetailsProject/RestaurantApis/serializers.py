from rest_framework.validators import UniqueValidator
#from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
#from django.contrib.auth.models import User
from HotelApis.models import *
from .models import *




#--------------------------------------------------------------

from rest_framework import serializers
#from django.contrib.auth.models import User

class RestaurantTablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantTables
        fields = '__all__'


class RestaurantInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantInventory
        fields = '__all__'


#------------------PRODUCTS UNIT----------------------------



class RestaurantProductsUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantProductsUnit
        fields = '__all__'


class RestaurantCategoriesSerializer(serializers.ModelSerializer):
    Unit = RestaurantProductsUnitSerializer(many=False)
    class Meta:
        model = RestaurantCategories
        fields = '__all__'





class RestaurantCustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCustomers
        fields = '__all__'










#HIZI NI KWAAJILI YA KUADD PRODUCTS KWASABABU TUKITUMIA HIZO ZA CHINI
#BILA KUTOA HIYO Unit FIELD INALETA ERROR SO  ILI KUAVOID HIYO ERROR
#TUNATUMIA HIZI KWAAJILI YA KUADD PRODUCT

class AddRestaurantProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantProducts
        fields = '__all__'




#MWISHO WA HIZO ZA KUADD PRODUCTS


#-----------------Restaurant  PRODUCTS------------------
class RestaurantProductsSerializer(serializers.ModelSerializer):
    Unit = RestaurantProductsUnitSerializer(many=False)
    class Meta:
        model = RestaurantProducts
        fields = '__all__'









#---------------------Restaurant  CART SERIALIZER---------


class RestaurantCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantCart
        fields = '__all__'


class RestaurantCartItemsSerializer(serializers.ModelSerializer):
    cart = RestaurantCartSerializer()
    product = RestaurantProductsSerializer()

    #table = RestaurantTablesSerializer()
    class Meta:
        model = RestaurantCartItems
        fields = '__all__'



class RestaurantOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantOrder
        fields = '__all__'


class RestaurantOrderItemsSerializer(serializers.ModelSerializer):
    order = RestaurantOrderSerializer()
    product = RestaurantProductsSerializer()

    table = RestaurantTablesSerializer()
    Customer = RestaurantCustomersSerializer()
    class Meta:
        model = RestaurantOrderItems
        fields = '__all__'













#-----------GET HOTEL WAITERS----------------
class RestaurantWaitersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'







