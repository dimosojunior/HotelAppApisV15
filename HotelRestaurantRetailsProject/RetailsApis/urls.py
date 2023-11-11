
from django.urls import path
from . import views

# MWANZO IN ORDER TO USE MODEL VIEW SET


urlpatterns = [
	#GET Retails CATEGORIES WITH CATEGORY ID
    path('AllRetailsCategories/', views.AllRetailsCategoriesView.as_view(), name='AllRetailsCategories'),

    path('RetailsProducts/', views.RetailsProductsViewSet.as_view(), name='RetailsProducts'),
    

    path('RetailsInventory/', views.RetailsInventoryViewSet.as_view(), name='RetailsInventory'),
    path('RetailsCategories/', views.RetailsCategoriesViewSet.as_view(), name='RetailsCategories'),
    
    #path('RoomsClasses/', views.RoomsClassesViewSet.as_view(), name='RoomsClasses'),
    path('RetailsCustomers/', views.RetailsCustomersViewSet.as_view(), name='RetailsCustomers'),
    path('MyUser/', views.MyUserViewSet.as_view(), name='MyUser'),
   
    

    

]
