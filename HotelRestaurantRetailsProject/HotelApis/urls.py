
from django.urls import path
from . import views



urlpatterns = [

    #GET HOTEL CATEGORIES WITH CATEGORY ID
    path('AllHotelCategories/', views.AllHotelCategoriesView.as_view(), name='AllHotelCategories'),

    path('HotelLocationCode/', views.HotelLocationCodeViewSet.as_view(), name='HotelLocationCode'),
    path('HotelBusinessUnit/', views.HotelBusinessUnitViewSet.as_view(), name='HotelBusinessUnit'),

    path('HotelProducts/', views.HotelProductsViewSet.as_view(), name='HotelProducts'),
    
    path('HotelRoomsProducts/', views.HotelRoomsProductsViewSet.as_view(), name='HotelRoomsProducts'),
    path('HotelBookedRoomsProducts/', views.HotelBookedRoomsProductsViewSet.as_view(), name='HotelBookedRoomsProducts'),



    path('HotelInventory/', views.HotelInventoryViewSet.as_view(), name='HotelInventory'),
    path('HotelCategories/', views.HotelCategoriesViewSet.as_view(), name='HotelCategories'),
    
    path('RoomsClasses/', views.RoomsClassesViewSet.as_view(), name='RoomsClasses'),
    path('HotelCustomers/', views.HotelCustomersViewSet.as_view(), name='HotelCustomers'),
    path('MyUser/', views.MyUserViewSet.as_view(), name='MyUser'),
   
    


    


    

]





