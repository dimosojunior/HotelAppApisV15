
from django.urls import path
from . import views

# MWANZO IN ORDER TO USE MODEL VIEW SET


urlpatterns = [

	#GET Restaurant CATEGORIES WITH CATEGORY ID
    path('AllRestaurantCategories/', views.AllRestaurantCategoriesView.as_view(), name='AllRestaurantCategories'),

    path('RestaurantProducts/', views.RestaurantProductsViewSet.as_view(), name='RestaurantProducts'),
    

    path('RestaurantInventory/', views.RestaurantInventoryViewSet.as_view(), name='RestaurantInventory'),
    path('RestaurantCategories/', views.RestaurantCategoriesViewSet.as_view(), name='RestaurantCategories'),
    
    #path('RoomsClasses/', views.RoomsClassesViewSet.as_view(), name='RoomsClasses'),
    path('RestaurantCustomers/', views.RestaurantCustomersViewSet.as_view(), name='RestaurantCustomers'),
    path('MyUser/', views.MyUserViewSet.as_view(), name='MyUser'),
   
    

    

]
