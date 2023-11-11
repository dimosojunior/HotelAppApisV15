from . import views
from django.urls import path,include

from rest_framework.routers import DefaultRouter






urlpatterns = [


    path('', views.HomeView, name='CartHome'),

    #-------------------HOTEL  CART---------------------------
    path('HotelCart/', views.HotelCartView.as_view(), name='HotelCart'),
    path('HotelOrder/', views.HotelOrderView.as_view(), name='hotel--order-list'),
    path('HotelOrdernNoDelete/', views.HotelOrdernNoDeleteView.as_view(), name='hotel--order-list-no-delete'),
    path('HotelDeleteCartItem/', views.HotelDeleteCartItemView.as_view(), name='HotelDeleteCart'),




    



    #-------------------HOTEL ROOMS---------------------------

    path('HotelRoomsCart/', views.HotelRoomsCartView.as_view(), name='HotelRoomsCart'),
    path('HotelRoomsOrder/', views.HotelRoomsOrderView.as_view(), name='hotel-Rooms-order-list'),
    path('HotelRoomsDeleteCartItem/', views.HotelRoomsDeleteCartItemView.as_view(), name='HotelRoomsDeleteCart'),
    #path('HotelRoomsOrdernNoDelete/', views.HotelRoomsOrdernNoDeleteView.as_view(), name='hotel-Rooms-order-list-no-delete'),


    















    #-------------------Restaurant  CART---------------------------
    path('RestaurantCart/', views.RestaurantCartView.as_view(), name='RestaurantCart'),
    path('RestaurantOrder/', views.RestaurantOrderView.as_view(), name='Restaurant--order-list'),
    path('RestaurantOrdernNoDelete/', views.RestaurantOrdernNoDeleteView.as_view(), name='Restaurant--order-list-no-delete'),
    path('RestaurantDeleteCartItem/', views.RestaurantDeleteCartItemView.as_view(), name='RestaurantDeleteCart'),
    #path('DeleteCartItem/', views.DeleteCartItemView.as_view(), name='DeleteCart'),




    











    #-------------------Retails  CART---------------------------
    path('RetailsCart/', views.RetailsCartView.as_view(), name='RetailsCart'),
    path('RetailsOrder/', views.RetailsOrderView.as_view(), name='Retails--order-list'),
    path('RetailsOrdernNoDelete/', views.RetailsOrdernNoDeleteView.as_view(), name='Retails--order-list-no-delete'),
    #path('DeleteCartItem/', views.DeleteCartItemView.as_view(), name='DeleteCart'),
    path('RetailsDeleteCartItem/', views.RetailsDeleteCartItemView.as_view(), name='RetailsDeleteCart'),




    






    #------------------HOTEL  REPORT--------------------
    path('HotelOrderReport/', views.HotelOrderReportView.as_view(), name='HotelOrderReport'),
    path('HotelRoomsOrderReport/', views.HotelRoomsOrderReportView.as_view(), name='HotelRoomsOrderReport'),
    





    #------------------RESTAURANT  REPORT--------------------
    path('RestaurantOrderReport/', views.RestaurantOrderReportView.as_view(), name='RestaurantOrderReport'),
    



    #------------------RETAILS  REPORT--------------------
    path('RetailsOrderReport/', views.RetailsOrderReportView.as_view(), name='RetailsOrderReport'),
    




    #------------------FILTER REPORT----------------------

    #----------HOTEL FILTER REPORT

    path('FilterHotelOrderReport/', views.FilterHotelOrderReportView.as_view(), name='FilterHotelOrderReport'),
    path('FilterHotelRoomsOrderReport/', views.FilterHotelRoomsOrderReportView.as_view(), name='FilterHotelRoomsOrderReport'),
    



    #__________RESTAURANT FILTER REPORT-----------------------
    path('FilterRestaurantOrderReport/', views.FilterRestaurantOrderReportView.as_view(), name='FilterRestaurantOrderReport'),
    





    #------------------RETAILS FILTER REPORT----------------

    path('FilterRetailsOrderReport/', views.FilterRetailsOrderReportView.as_view(), name='FilterRetailsOrderReport'),
    
    



    
    

    #------------------RECEIPT------------------------

    #-----------HOTEL  RECEIPT-------------------
    path('HotelReceipt/', views.HotelReceiptView.as_view(), name='HotelReceipt'),










    #---------------------------GET ALL ORDER ITEMS  HOTEL ----------------------
    path('GetHotelOrderItems/', views.GetHotelOrderItemsView.as_view(), name='GetHotelOrderItems'),
    path('GetHotelRoomsOrderItems/', views.GetHotelRoomsOrderItemsView.as_view(), name='GetHotelRoomsOrderItems'),
    



    #---------------------------GET ALL ORDER ITEMS  Restaurant ----------------------
    path('GetRestaurantOrderItems/', views.GetRestaurantOrderItemsView.as_view(), name='GetRestaurantOrderItems'),
    



    #---------------------------GET ALL ORDER ITEMS  Retails ----------------------
    path('GetRetailsOrderItems/', views.GetRetailsOrderItemsView.as_view(), name='GetRetailsOrderItems'),
    






    #----------------CHANGE ORDERSTATUS----------------------
    #---------------HOTEL -----------------------
    path('HotelOrderChangeStatusToTrue/', views.HotelOrderChangeStatusToTrueView.as_view(), name='HotelOrderChangeStatusToTrue'),
    path('HotelOrderChangeStatusToFalse/', views.HotelOrderChangeStatusToFalseView.as_view(), name='HotelOrderChangeStatusToFalse'),

    
    path('HotelRoomsOrderChangeStatusToTrue/', views.HotelRoomsOrderChangeStatusToTrueView.as_view(), name='HotelRoomsOrderChangeStatusToTrue'),
    path('HotelRoomsOrderChangeStatusToFalse/', views.HotelRoomsOrderChangeStatusToFalseView.as_view(), name='HotelRoomsOrderChangeStatusToFalse'),

    

    #-----------------RESTAURANT------------------------
    path('RestaurantOrderChangeStatusToTrue/', views.RestaurantOrderChangeStatusToTrueView.as_view(), name='RestaurantOrderChangeStatusToTrue'),
    path('RestaurantOrderChangeStatusToFalse/', views.RestaurantOrderChangeStatusToFalseView.as_view(), name='RestaurantOrderChangeStatusToFalse'),

    


    #---------------------------RETAILS----------------------
    path('RetailsOrderChangeStatusToTrue/', views.RetailsOrderChangeStatusToTrueView.as_view(), name='RetailsOrderChangeStatusToTrue'),
    path('RetailsOrderChangeStatusToFalse/', views.RetailsOrderChangeStatusToFalseView.as_view(), name='RetailsOrderChangeStatusToFalse'),

    







    #------------------DELETE ORDERS-----------------------

    #---------DELETE HOTEL ORDERED ITEMS----------------
    path('HotelDeleteOrderItem/', views.HotelDeleteOrderItemView.as_view(), name='HotelDeleteOrderItem'),
    path('HotelRoomsDeleteOrderItem/', views.HotelRoomsDeleteOrderItemView.as_view(), name='HotelRoomsDeleteOrderItem'),
    


    #---------DELETE Restaurant ORDERED ITEMS----------------
    path('RestaurantDeleteOrderItem/', views.RestaurantDeleteOrderItemView.as_view(), name='RestaurantDeleteOrderItem'),
    

    #---------DELETE Retails ORDERED ITEMS----------------
    path('RetailsDeleteOrderItem/', views.RetailsDeleteOrderItemView.as_view(), name='RetailsDeleteOrderItem'),
    















    #-------------------------ADD TO CART MAKE ORDER WITHOUT ROOM BUT BY USING TABLEONLY
    path('HotelAddToCartWithoutRoom/', views.HotelAddToCartWithoutRoomView.as_view(), name='HotelAddToCartWithoutRoom'),
    
    path('RestaurantAddToCartWithoutRoom/', views.RestaurantAddToCartWithoutRoomView.as_view(), name='RestaurantAddToCartWithoutRoom'),
    
    path('RetailsAddToCartWithoutRoom/', views.RetailsAddToCartWithoutRoomView.as_view(), name='RetailsAddToCartWithoutRoom'),
    










    #------------------MAKE ORDER WITH ROOM-----------------
    path('MakeHotelOrderWithRoom/', views.MakeHotelOrderWithRoomView.as_view(), name='MakeHotelOrderWithRoom'),
    

    path('PlusRoom_MakeHotelOrderWithRoom/', views.PlusRoom_MakeHotelOrderWithRoomView.as_view(), name='PlusRoom_MakeHotelOrderWithRoom'),
    






    #-------------------COUNT ORDERS---------------------
    path('CountHotelOrder/', views.CountHotelOrderView.as_view(), name='CountHotelOrder'),
    path('CountHotelRoomsOrder/', views.CountHotelRoomsOrderView.as_view(), name='CountHotelRoomsOrder'),
    


    path('CountRestaurantOrder/', views.CountRestaurantOrderView.as_view(), name='CountRestaurantOrder'),
    



    path('CountRetailsOrder/', views.CountRetailsOrderView.as_view(), name='CountRetailsOrder'),
    






    #-----------CLOSE BILLS URLS----------------------

    path('HotelOrderCloseBill/', views.HotelOrderCloseBillView.as_view(), name='HotelOrderCloseBill'),
    path('HotelRoomsOrderCloseBill/', views.HotelRoomsOrderCloseBillView.as_view(), name='HotelRoomsOrderCloseBill'),
    

    path('RestaurantOrderCloseBill/', views.RestaurantOrderCloseBillView.as_view(), name='RestaurantOrderCloseBill'),
    

    path('RetailsOrderCloseBill/', views.RetailsOrderCloseBillView.as_view(), name='RetailsOrderCloseBill'),
    





#---------------------HOTEL GUEST CUSTOMERS----------------


    #------------REPORTS FOR GUEST CUSTOMERS-------------
    path('HotelGuestOrderReport/', views.HotelGuestOrderReportView.as_view(), name='HotelGuestOrderReport'),
    
    path('HotelGuestOrdersForSpecificUser/', views.HotelGuestOrdersForSpecificUserView.as_view(), name='HotelGuestOrdersForSpecificUser'),
    
    #---------FILTER REPORT FOR GUEST CUSTOMERS----------------
    path('FilterHotelGuestOrderReport/', views.FilterHotelGuestOrderReportView.as_view(), name='FilterHotelGuestOrderReport'),
    
    #-------------COUNT HOTEL ORDERS FOR GUEST CUSTOMERS---------------
    path('CountHotelGuestOrder/', views.CountHotelGuestOrderView.as_view(), name='CountHotelGuestOrder'),
    

    #------------GET ALL ORDERED ITEMS FOR GUEST CUSTOMERS-------------
    path('GetHotelGuestOrderItems/', views.GetHotelGuestOrderItemsView.as_view(), name='GetHotelGuestOrderItems'),
    










    ##--------------------COUNT ORDER FOR A SPECIFIC UESR/WAITER
    path('CountHotelOrderForEachUser/', views.CountHotelOrderForEachUserView.as_view(), name='CountHotelOrderForEachUser'),
    path('CountHotelRoomsOrderForEachUser/', views.CountHotelRoomsOrderForEachUserView.as_view(), name='CountHotelRoomsOrderForEachUser'),


    path('CountRestaurantOrderForEachUser/', views.CountRestaurantOrderForEachUserView.as_view(), name='CountRestaurantOrderForEachUser'),
    

    path('CountRetailsOrderForEachUser/', views.CountRetailsOrderForEachUserView.as_view(), name='CountRetailsOrderForEachUser'),
    


    ##--------------------FOR GUEST CUSTOMERS COUNT ORDER FOR A SPECIFIC UESR/WAITER
    path('CountHotelGuestOrderForEachUser/', views.CountHotelGuestOrderForEachUserView.as_view(), name='CountHotelGuestOrderForEachUser'),
    

]

