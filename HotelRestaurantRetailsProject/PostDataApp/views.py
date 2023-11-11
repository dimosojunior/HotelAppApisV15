from django.shortcuts import render
from django.shortcuts import render,redirect

from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render,get_object_or_404


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#REST FRAMEWORK
from rest_framework import status
from rest_framework.response import Response

#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView


#------------------------GENERIC VIEWs-------------------
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


#------------------------ VIEW SETS-------------------
from rest_framework.viewsets import ModelViewSet


#------FILTERS, SEARCH AND ORDERING
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter,OrderingFilter

#------PAGINATION-------------
from rest_framework.pagination import PageNumberPagination




#----------------CREATING A CART------------------------
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet


from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics,status
from rest_framework.decorators import api_view

# Create your views here.

# class UserView(APIView):

# 	def get(self,request, format=None):
# 		return Response("User Account View", status=200)

# 	def post(self,request, format=None):

# 		return Response("Creating User", status=200)



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed










#-----------------------------------------------


from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from HotelApis.models import MyUser  # Make sure to import your MyUser model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated







from django.shortcuts import render,get_object_or_404

from HotelApis.models import *
from RestaurantApis.models import *
from RetailsApis.models import *

from RetailsApis.serializers import *
from RestaurantApis.serializers import *
from HotelApis.serializers import *

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def HotelView(request):

	return HttpResponse("Hotel")







class MyUserViewSet(ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = MyUserSerializer


class HotelTablesViewSet(ModelViewSet):
    queryset = HotelTables.objects.filter(
        TableStatus=False
        )
    serializer_class = HotelTablesSerializer

class RestaurantTablesViewSet(ModelViewSet):
    queryset = RestaurantTables.objects.filter(
        TableStatus=False
        )
    serializer_class = RestaurantTablesSerializer


class RetailsTablesViewSet(ModelViewSet):
    queryset = RetailsTables.objects.filter(
        TableStatus=False
        )
    serializer_class = RetailsTablesSerializer







class HotelInventoryViewSet(ModelViewSet):
    queryset = HotelInventory.objects.all()
    serializer_class = HotelInventorySerializer    

class HotelCategoriesViewSet(ModelViewSet):
    queryset = HotelCategories.objects.all()
    serializer_class = HotelCategoriesSerializer 



class RoomsClassesViewSet(ModelViewSet):
    queryset = RoomsClasses.objects.all()
    serializer_class = RoomsClassesSerializer


class HotelCustomersViewSet(ModelViewSet):
    queryset = HotelCustomers.objects.all()
    serializer_class = HotelCustomersSerializer







#-------------HOTEL  PRODUCT-----------------
class HotelProductsViewSet(ModelViewSet):
    queryset = HotelProducts.objects.all()
    serializer_class = HotelProductsSerializer



class HotelRoomsViewSet(ModelViewSet):
    queryset = HotelRooms.objects.all()
    serializer_class = HotelRoomsSerializer

    #pagination_class = PageNumberPagination



#KWA AJILI YA KUADD PRODUCTS
class AddHotelProductsViewSet(ModelViewSet):
    queryset = HotelProducts.objects.all()
    serializer_class = AddHotelProductsSerializer


class AddHotelRoomsViewSet(ModelViewSet):
    queryset = HotelRooms.objects.all()
    serializer_class = AddHotelRoomsSerializer






#------------------UNORDERED ROOMS VIEWS------------------------
































#----------------------RESTAURANT-----------------------




class RestaurantInventoryViewSet(ModelViewSet):
    queryset = RestaurantInventory.objects.all()
    serializer_class = RestaurantInventorySerializer 


class RestaurantCategoriesViewSet(ModelViewSet):
    queryset = RestaurantCategories.objects.all()
    serializer_class = RestaurantCategoriesSerializer 


class RestaurantCustomersViewSet(ModelViewSet):
    queryset = RestaurantCustomers.objects.all()
    serializer_class = RestaurantCustomersSerializer















#--------------------------PRODCTS ZENYEWE--------------------





#-------------Restaurant  PRODUCT-----------------
class RestaurantProductsViewSet(ModelViewSet):
    queryset = RestaurantProducts.objects.all()
    serializer_class = RestaurantProductsSerializer





#KWA AJILI YA KUADD PRODUCTS
class AddRestaurantProductsViewSet(ModelViewSet):
    queryset = RestaurantProducts.objects.all()
    serializer_class = AddRestaurantProductsSerializer






















#------------------------RETAILS----------------------------





class RetailsInventoryViewSet(ModelViewSet):
    queryset = RetailsInventory.objects.all()
    serializer_class = RetailsInventorySerializer 

class RetailsCategoriesViewSet(ModelViewSet):
    queryset = RetailsCategories.objects.all()
    serializer_class = RetailsCategoriesSerializer



class RetailsCustomersViewSet(ModelViewSet):
    queryset = RetailsCustomers.objects.all()
    serializer_class = RetailsCustomersSerializer










#---------------FILTER WAITERS------------------------------

class HotelWaitersViewSet(ModelViewSet):
    queryset = MyUser.objects.filter(
        #is_waiter = True,
        is_hotel_user = True,
        is_admin=False
        )
    serializer_class = HotelWaitersSerializer


class RestaurantWaitersViewSet(ModelViewSet):
    queryset = MyUser.objects.filter(
        #is_waiter = True,
        is_restaurant_user = True,
        is_admin=False
        )
    serializer_class = RestaurantWaitersSerializer


class RetailsWaitersViewSet(ModelViewSet):
    queryset = MyUser.objects.filter(
        #is_waiter = True,
        is_retails_user = True,
        is_admin=False
        )
    serializer_class = RetailsWaitersSerializer
































#--------------------------PRODCTS ZENYEWE--------------------





#-------------Retails  PRODUCT-----------------
class RetailsProductsViewSet(ModelViewSet):
    queryset = RetailsProducts.objects.all()
    serializer_class = RetailsProductsSerializer



#KWA AJILI YA KUADD PRODUCTS
class AddRetailsProductsViewSet(ModelViewSet):
    queryset = RetailsProducts.objects.all()
    serializer_class = AddRetailsProductsSerializer







#----------------PRODUCTS UNIT------------------------------

#----------------HOTEL PRODUCTS UNIT------------------------
class HotelProductsUnitViewSet(ModelViewSet):
    queryset = HotelProductsUnit.objects.all()
    serializer_class = HotelProductsUnitSerializer



#----------------RESTAURANT PRODUCTS UNIT------------------------
class RestaurantProductsUnitViewSet(ModelViewSet):
    queryset = RestaurantProductsUnit.objects.all()
    serializer_class = RestaurantProductsUnitSerializer


#----------------RETAILS PRODUCTS UNIT------------------------
class RetailsProductsUnitViewSet(ModelViewSet):
    queryset = RetailsProductsUnit.objects.all()
    serializer_class = RetailsProductsUnitSerializer