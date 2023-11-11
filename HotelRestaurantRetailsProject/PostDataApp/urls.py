
from django.urls import path
from . import views

# # MWANZO IN ORDER TO USE MODEL VIEW SET
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('PostMyUser', views.MyUserViewSet)
router.register('PostHotelTables', views.HotelTablesViewSet)
router.register('PostRestaurantTables', views.RestaurantTablesViewSet)
router.register('PostRetailsTables', views.RetailsTablesViewSet)



router.register('PostHotelInventory', views.HotelInventoryViewSet)
router.register('PostHotelCategories', views.HotelCategoriesViewSet)

router.register('PostRoomsClasses', views.RoomsClassesViewSet)
router.register('PostHotelCustomers', views.HotelCustomersViewSet)




# HOTEL  PRODUCT
router.register('PostHotelProducts', views.HotelProductsViewSet)

router.register('PostHotelRooms', views.HotelRoomsViewSet)

#Kwa ajili ya kuadd products
router.register('PostAddHotelProducts', views.AddHotelProductsViewSet)

router.register('PostAddHotelRooms', views.AddHotelRoomsViewSet)


















#-----------------------RESTAURANT----------------------


router.register('PostRestaurantInventory', views.RestaurantInventoryViewSet)
router.register('PostRestaurantCategories', views.RestaurantCategoriesViewSet)

#Kwa ajili ya kuadd products
router.register('PostAddRestaurantProducts', views.AddRestaurantProductsViewSet)

router.register('PostRestaurantCustomers', views.RestaurantCustomersViewSet)






# REstaurant  PRODUCT
router.register('PostRestaurantProducts', views.RestaurantProductsViewSet)












#-----------------------RETAILS-------------------------




router.register('PostRetailsInventory', views.RetailsInventoryViewSet)
router.register('PostRetailsCategories', views.RetailsCategoriesViewSet)


#Kwa ajili ya kuadd products
router.register('PostAddRetailsProducts', views.AddRetailsProductsViewSet)

router.register('PostRetailsCustomers', views.RetailsCustomersViewSet)












# RETAILS  PRODUCT
router.register('PostRetailsProducts', views.RetailsProductsViewSet)








#---------------GET WAITERS---------------------

router.register('PostHotelWaiters', views.HotelWaitersViewSet)
router.register('PostRestaurantWaiters', views.RestaurantWaitersViewSet)
router.register('PostRetailsWaiters', views.RetailsWaitersViewSet)







#-------------PRODUCTS UNIT------------------------------
router.register('PostHotelProductsUnit', views.HotelProductsUnitViewSet)
router.register('PostRestaurantProductsUnit', views.RestaurantProductsUnitViewSet)
router.register('PostRetailsProductsUnit', views.RetailsProductsUnitViewSet)





urlpatterns = router.urls