from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('RestaurantHomePage/', views.RestaurantHomePage, name='RestaurantHomePage'),

    path('RestaurantDeactivateUsersPage/', views.RestaurantDeactivateUsersPage, name='RestaurantDeactivateUsersPage'),
    path('Restaurantdeactivate_inactive_users/', views.Restaurantdeactivate_inactive_users, name='Restaurantdeactivate_inactive_users'),

    path('Restaurant_search_username_UnpaidRestaurantMyUser_autocomplete/', views.Restaurant_search_username_UnpaidRestaurantMyUser_autocomplete, name='Restaurant_search_username_UnpaidRestaurantMyUser_autocomplete'),
    path('Restaurant_search_email_UnpaidRestaurantMyUser_autocomplete/', views.Restaurant_search_email_UnpaidRestaurantMyUser_autocomplete, name='Restaurant_search_email_UnpaidRestaurantMyUser_autocomplete'),
    path('Restaurant_search_company_name_UnpaidRestaurantMyUser_autocomplete/', views.Restaurant_search_company_name_UnpaidRestaurantMyUser_autocomplete, name='Restaurant_search_company_name_UnpaidRestaurantMyUser_autocomplete'),
    path('UpdateUnpaidRestaurantMyUser/<int:id>/', views.UpdateUnpaidRestaurantMyUser, name='UpdateUnpaidRestaurantMyUser'),




    path('RestaurantactivateUsersPage/', views.RestaurantactivateUsersPage, name='RestaurantactivateUsersPage'),
    path('Restaurantactivate_inactive_users/', views.Restaurantactivate_inactive_users, name='Restaurantactivate_inactive_users'),

    path('Restaurant_search_username_paidRestaurantMyUser_autocomplete/', views.Restaurant_search_username_paidRestaurantMyUser_autocomplete, name='Restaurant_search_username_paidRestaurantMyUser_autocomplete'),
    path('Restaurant_search_email_paidRestaurantMyUser_autocomplete/', views.Restaurant_search_email_paidRestaurantMyUser_autocomplete, name='Restaurant_search_email_paidRestaurantMyUser_autocomplete'),
    path('Restaurant_search_company_name_paidRestaurantMyUser_autocomplete/', views.Restaurant_search_company_name_paidRestaurantMyUser_autocomplete, name='Restaurant_search_company_name_paidRestaurantMyUser_autocomplete'),
    path('UpdatepaidRestaurantMyUser/<int:id>/', views.UpdatepaidRestaurantMyUser, name='UpdatepaidRestaurantMyUser'),


    path('RestaurantSignupPage/', views.RestaurantSignupPage, name='RestaurantSignupPage'),
    path('RestaurantUpdateUser/<int:id>/', views.RestaurantUpdateUser, name='RestaurantUpdateUser'),
    # path('', views.SigninPage, name='SigninPage'),


#-------------RESET PASSWORD
    # path('reset_password/', 
    #     auth_views.PasswordResetView.as_view(template_name="Account/password_reset.html"), 
    #     name="reset_password"),

    # path('reset_password_sent/', 
    #     auth_views.PasswordResetDoneView.as_view(template_name="Account/password_reset_sent.html"),
    #      name="password_reset_done"),


    # path('reset/<uidb64>/<token>/', 
    #     auth_views.PasswordResetConfirmView.as_view(template_name="Account/password_reset_form.html"),
    #     name="password_reset_confirm"),
    

    # path('reset_password_complete/', 
    #     auth_views.PasswordResetCompleteView.as_view(template_name="Account/password_reset_done.html"),
    #  name="password_reset_complete"),




    #--------CHANGE PASSWORD
    path('Restaurantchange_password/', views.RestaurantPasswordChangeView.as_view(template_name = "Account/Restaurantpassword_change.html"), name="Restaurantchange-password"),


    # path('LogoutPage/', views.LogoutPage, name='LogoutPage'),





    #------------------ALL Restaurant USERS------------------------

    #path('AllUnpaidRestaurantMyUserPage/', views.AllUnpaidRestaurantMyUserPage, name='AllUnpaidRestaurantMyUserPage'),




    path('RestaurantCustomersPage/', views.RestaurantCustomersPage, name='RestaurantCustomersPage'),
    path('Restaurant_search_customer_autocomplete/', views.Restaurant_search_customer_autocomplete, name='Restaurant_search_customer_autocomplete'),
    path('Restaurant_search_address_autocomplete/', views.Restaurant_search_address_autocomplete, name='Restaurant_search_address_autocomplete'),
    path('DeleteRestaurantCustomerPage/<int:id>/', views.DeleteRestaurantCustomerPage, name='DeleteRestaurantCustomerPage'),
    path('AddRestaurantCustomerPage/', views.AddRestaurantCustomerPage, name='AddRestaurantCustomerPage'),
    path('UpdateRestaurantCustomerPage/<int:id>/', views.UpdateRestaurantCustomerPage, name='UpdateRestaurantCustomerPage'),




    #---------------Restaurant BUSINESS UNIT-----------------------
    path('RestaurantBusinessUnitPage/', views.RestaurantBusinessUnitPage, name='RestaurantBusinessUnitPage'),
    path('Restaurant_search_Code_Business_Unit_autocomplete/', views.Restaurant_search_Code_Business_Unit_autocomplete, name='Restaurant_search_Code_Business_Unit_autocomplete'),
    path('Restaurant_search_Description_Business_Unit_autocomplete/', views.Restaurant_search_Description_Business_Unit_autocomplete, name='Restaurant_search_Description_Business_Unit_autocomplete'),
    path('DeleteRestaurantBusinessUnit/<int:id>/', views.DeleteRestaurantBusinessUnit, name='DeleteRestaurantBusinessUnit'),
    path('AddRestaurantBusinessUnit/', views.AddRestaurantBusinessUnit, name='AddRestaurantBusinessUnit'),
    path('UpdateRestaurantBusinessUnit/<int:id>/', views.UpdateRestaurantBusinessUnit, name='UpdateRestaurantBusinessUnit'),




    #---------------Restaurant LOCATION CODES-----------------------
    path('RestaurantLocationCodePage/', views.RestaurantLocationCodePage, name='RestaurantLocationCodePage'),
    path('Restaurant_search_Code_Location_Code_autocomplete/', views.Restaurant_search_Code_Location_Code_autocomplete, name='Restaurant_search_Code_Location_Code_autocomplete'),
    path('Restaurant_search_Description_Location_Code_autocomplete/', views.Restaurant_search_Description_Location_Code_autocomplete, name='Restaurant_search_Description_Location_Code_autocomplete'),
    path('DeleteRestaurantLocationCode/<int:id>/', views.DeleteRestaurantLocationCode, name='DeleteRestaurantLocationCode'),
    path('AddRestaurantLocationCode/', views.AddRestaurantLocationCode, name='AddRestaurantLocationCode'),
    path('UpdateRestaurantLocationCode/<int:id>/', views.UpdateRestaurantLocationCode, name='UpdateRestaurantLocationCode'),




    #---------------Restaurant PROCESS CONFIG-----------------------
    path('RestaurantProcessConfigPage/', views.RestaurantProcessConfigPage, name='RestaurantProcessConfigPage'),
    path('Restaurant_search_ProcesId_process_config_autocomplete/', views.Restaurant_search_ProcesId_process_config_autocomplete, name='Restaurant_search_ProcesId_process_config_autocomplete'),
    path('Restaurant_search_Description_process_config_autocomplete/', views.Restaurant_search_Description_process_config_autocomplete, name='Restaurant_search_Description_process_config_autocomplete'),
    path('DeleteRestaurantProcessConfig/<int:id>/', views.DeleteRestaurantProcessConfig, name='DeleteRestaurantProcessConfig'),
    path('AddRestaurantProcessConfig/', views.AddRestaurantProcessConfig, name='AddRestaurantProcessConfig'),
    path('UpdateRestaurantProcessConfig/<int:id>/', views.UpdateRestaurantProcessConfig, name='UpdateRestaurantProcessConfig'),


    #---------------Restaurant STORE CODES-----------------------
    path('RestaurantStoreCodePage/', views.RestaurantStoreCodePage, name='RestaurantStoreCodePage'),
    path('Restaurant_search_Code_store_code_autocomplete/', views.Restaurant_search_Code_store_code_autocomplete, name='Restaurant_search_Code_store_code_autocomplete'),
    path('Restaurant_search_Description_store_code_autocomplete/', views.Restaurant_search_Description_store_code_autocomplete, name='Restaurant_search_Description_store_code_autocomplete'),
    path('DeleteRestaurantStoreCode/<int:id>/', views.DeleteRestaurantStoreCode, name='DeleteRestaurantStoreCode'),
    path('AddRestaurantStoreCode/', views.AddRestaurantStoreCode, name='AddRestaurantStoreCode'),
    path('UpdateRestaurantStoreCode/<int:id>/', views.UpdateRestaurantStoreCode, name='UpdateRestaurantStoreCode'),




    #---------------Restaurant STORE BIN CODES-----------------------
    path('RestaurantStoreBinCodePage/', views.RestaurantStoreBinCodePage, name='RestaurantStoreBinCodePage'),
    path('Restaurant_search_StoreBinCode_store_bin_code_autocomplete/', views.Restaurant_search_StoreBinCode_store_bin_code_autocomplete, name='Restaurant_search_StoreBinCode_store_bin_code_autocomplete'),
    path('Restaurant_search_CardNo_store_bin_code_autocomplete/', views.Restaurant_search_CardNo_store_bin_code_autocomplete, name='Restaurant_search_CardNo_store_bin_code_autocomplete'),
    path('Restaurant_search_Description_store_bin_code_autocomplete/', views.Restaurant_search_Description_store_bin_code_autocomplete, name='Restaurant_search_Description_store_bin_code_autocomplete'),
    path('DeleteRestaurantStoreBinCode/<int:id>/', views.DeleteRestaurantStoreBinCode, name='DeleteRestaurantStoreBinCode'),
    path('AddRestaurantStoreBinCode/', views.AddRestaurantStoreBinCode, name='AddRestaurantStoreBinCode'),
    path('UpdateRestaurantStoreBinCode/<int:id>/', views.UpdateRestaurantStoreBinCode, name='UpdateRestaurantStoreBinCode'),



    #---------------Restaurant EVENT CODES-----------------------
    path('RestaurantEventCodePage/', views.RestaurantEventCodePage, name='RestaurantEventCodePage'),
    path('Restaurant_search_Code_Event_Code_autocomplete/', views.Restaurant_search_Code_Event_Code_autocomplete, name='Restaurant_search_Code_Event_Code_autocomplete'),
    path('Restaurant_search_Description_Event_Code_autocomplete/', views.Restaurant_search_Description_Event_Code_autocomplete, name='Restaurant_search_Description_Event_Code_autocomplete'),
    path('DeleteRestaurantEventCode/<int:id>/', views.DeleteRestaurantEventCode, name='DeleteRestaurantEventCode'),
    path('AddRestaurantEventCode/', views.AddRestaurantEventCode, name='AddRestaurantEventCode'),
    path('UpdateRestaurantEventCode/<int:id>/', views.UpdateRestaurantEventCode, name='UpdateRestaurantEventCode'),



    #---------------Restaurant EVENT ALERT-----------------------
    path('RestaurantEventAlertPage/', views.RestaurantEventAlertPage, name='RestaurantEventAlertPage'),
    path('Restaurant_search_Code_AlertID_autocomplete/', views.Restaurant_search_Code_AlertID_autocomplete, name='Restaurant_search_Code_AlertID_autocomplete'),
    path('DeleteRestaurantEventAlert/<int:id>/', views.DeleteRestaurantEventAlert, name='DeleteRestaurantEventAlert'),
    path('AddRestaurantEventAlert/', views.AddRestaurantEventAlert, name='AddRestaurantEventAlert'),
    path('UpdateRestaurantEventAlert/<int:id>/', views.UpdateRestaurantEventAlert, name='UpdateRestaurantEventAlert'),




    #---------------Restaurant UOM SHORT CODES-----------------------
    path('RestaurantUOMPage/', views.RestaurantUOMPage, name='RestaurantUOMPage'),
    path('Restaurant_search_UOMShortCode_RestaurantUOM_autocomplete/', views.Restaurant_search_UOMShortCode_RestaurantUOM_autocomplete, name='Restaurant_search_UOMShortCode_RestaurantUOM_autocomplete'),
    path('DeleteRestaurantUOM/<int:id>/', views.DeleteRestaurantUOM, name='DeleteRestaurantUOM'),
    path('AddRestaurantUOM/', views.AddRestaurantUOM, name='AddRestaurantUOM'),
    path('UpdateRestaurantUOM/<int:id>/', views.UpdateRestaurantUOM, name='UpdateRestaurantUOM'),



    #---------------Restaurant UOM SHORT CODES-----------------------
    path('RestaurantBOMPage/', views.RestaurantBOMPage, name='RestaurantBOMPage'),
    path('Restaurant_search_Code_RestaurantBOM_autocomplete/', views.Restaurant_search_Code_RestaurantBOM_autocomplete, name='Restaurant_search_Code_RestaurantBOM_autocomplete'),
    path('Restaurant_search_Name_RestaurantBOM_autocomplete/', views.Restaurant_search_Name_RestaurantBOM_autocomplete, name='Restaurant_search_Name_RestaurantBOM_autocomplete'),
    path('DeleteRestaurantBOM/<int:id>/', views.DeleteRestaurantBOM, name='DeleteRestaurantBOM'),
    path('AddRestaurantBOM/', views.AddRestaurantBOM, name='AddRestaurantBOM'),
    path('UpdateRestaurantBOM/<int:id>/', views.UpdateRestaurantBOM, name='UpdateRestaurantBOM'),

    path('RestaurantBOMDetailPage/', views.RestaurantBOMDetailPage, name='RestaurantBOMDetailPage'),
    path('AddRestaurantBOMFiles/', views.AddRestaurantBOMFiles, name='AddRestaurantBOMFiles'),







    #-------------------HOTE L PRODUCTS CATEGORY----------------
    #-----All Categories----------
    path('RestaurantProductsCategoriesPage/', views.RestaurantProductsCategoriesPage, name='RestaurantProductsCategoriesPage'),

    path('ViewRestaurantCategoriesPage/<int:id>/', views.ViewRestaurantCategoriesPage, name='ViewRestaurantCategoriesPage'),
    path('UpdateRestaurantCategories/<int:id>/', views.UpdateRestaurantCategories, name='UpdateRestaurantCategories'),
    path('DeleteRestaurantCategories/<int:id>/', views.DeleteRestaurantCategories, name='DeleteRestaurantCategories'),


    #-------------------Restaurant DRINKS  PRODUCTS CATEGORIES-------------
    path('ViewRestaurantDrinksCategoriesPage/<int:id>/', views.ViewRestaurantDrinksCategoriesPage, name='ViewRestaurantDrinksCategoriesPage'),
    path('UpdateRestaurantDrinksCategories/<int:id>/', views.UpdateRestaurantDrinksCategories, name='UpdateRestaurantDrinksCategories'),
    path('DeleteRestaurantDrinksCategories/<int:id>/', views.DeleteRestaurantDrinksCategories, name='DeleteRestaurantDrinksCategories'),



    








    #---------------------PRODUCTS ITSELF MAINTENANCE---------

    path('RestaurantProductsPage/', views.RestaurantProductsPage, name='RestaurantProductsPage'),
    

    #-------------------- PRODUCTS-------------
    path('RestaurantProductsPage/', views.RestaurantProductsPage, name='RestaurantProductsPage'),
    path('search_product_name_RestaurantProducts_autocomplete/', views.search_product_name_RestaurantProducts_autocomplete, name='search_product_name_RestaurantProducts_autocomplete'),
    path('search_product_second_name_RestaurantProducts_autocomplete/', views.search_product_second_name_RestaurantProducts_autocomplete, name='search_product_second_name_RestaurantProducts_autocomplete'),
    path('AddRestaurantProducts/', views.AddRestaurantProducts, name='AddRestaurantProducts'),
    path('DeleteRestaurantProducts/<int:id>/', views.DeleteRestaurantProducts, name='DeleteRestaurantProducts'),
    path('UpdateRestaurantProducts/<int:id>/', views.UpdateRestaurantProducts, name='UpdateRestaurantProducts'),

    #--------------------DRINKS PRODUCTS-------------
    path('RestaurantDrinksProductsPage/', views.RestaurantDrinksProductsPage, name='RestaurantDrinksProductsPage'),
    path('search_product_name_RestaurantDrinksProducts_autocomplete/', views.search_product_name_RestaurantDrinksProducts_autocomplete, name='search_product_name_RestaurantDrinksProducts_autocomplete'),
    path('search_product_second_name_RestaurantDrinksProducts_autocomplete/', views.search_product_second_name_RestaurantDrinksProducts_autocomplete, name='search_product_second_name_RestaurantDrinksProducts_autocomplete'),
    path('AddRestaurantDrinksProducts/', views.AddRestaurantDrinksProducts, name='AddRestaurantDrinksProducts'),
    path('DeleteRestaurantDrinksProducts/<int:id>/', views.DeleteRestaurantDrinksProducts, name='DeleteRestaurantDrinksProducts'),
    path('UpdateRestaurantDrinksProducts/<int:id>/', views.UpdateRestaurantDrinksProducts, name='UpdateRestaurantDrinksProducts'),




    







    #----------------UPLOAD PRODUCTS----------------------------------------
    path('UploadRestaurantProductsPage/', views.UploadRestaurantProductsPage, name='UploadRestaurantProductsPage'),
    
    path('UploadRestaurantProductsPage/', views.UploadRestaurantProductsPage, name='UploadRestaurantProductsPage'),
    path('UploadRestaurantDrinksProductsPage/', views.UploadRestaurantDrinksProductsPage, name='UploadRestaurantDrinksProductsPage'),
    





    #------------------------------ORDERS--------------------------------

    path('RestaurantOrdersPage/', views.RestaurantOrdersPage, name='RestaurantOrdersPage'),

    #-------------Restaurant  ORDERS----------------------------------
    path('RestaurantOrderPage/', views.RestaurantOrderPage, name='RestaurantOrderPage'),
    path('DeleteRestaurantOrder/<int:id>/', views.DeleteRestaurantOrder, name='DeleteRestaurantOrder'),

    #-------------Restaurant Drinks ORDERS----------------------------------
    path('RestaurantDrinksOrderPage/', views.RestaurantDrinksOrderPage, name='RestaurantDrinksOrderPage'),
    path('DeleteRestaurantDrinksOrder/<int:id>/', views.DeleteRestaurantDrinksOrder, name='DeleteRestaurantDrinksOrder'),

    




    


    #------------------------STAFF MAINTENANCE_-----------------
    path('RestaurantMyUserPage/', views.RestaurantMyUserPage, name='RestaurantMyUserPage'),
    path('Restaurant_search_username_RestaurantMyUser_autocomplete/', views.Restaurant_search_username_RestaurantMyUser_autocomplete, name='Restaurant_search_username_RestaurantMyUser_autocomplete'),
    path('Restaurant_search_email_RestaurantMyUser_autocomplete/', views.Restaurant_search_email_RestaurantMyUser_autocomplete, name='Restaurant_search_email_RestaurantMyUser_autocomplete'),
    path('DeleteRestaurantMyUser/<int:id>/', views.DeleteRestaurantMyUser, name='DeleteRestaurantMyUser'),





    #--------------------Restaurant SUPPLIERS_------------------------

    path('RestaurantSuppliersPage/', views.RestaurantSuppliersPage, name='RestaurantSuppliersPage'),
    path('Restaurant_search_SupplierFullName_RestaurantSuppliers_autocomplete/', views.Restaurant_search_SupplierFullName_RestaurantSuppliers_autocomplete, name='Restaurant_search_SupplierFullName_RestaurantSuppliers_autocomplete'),
    path('Restaurant_search_Keyword_RestaurantSuppliers_autocomplete/', views.Restaurant_search_Keyword_RestaurantSuppliers_autocomplete, name='Restaurant_search_Keyword_RestaurantSuppliers_autocomplete'),
    path('DeleteRestaurantSuppliers/<int:id>/', views.DeleteRestaurantSuppliers, name='DeleteRestaurantSuppliers'),
    path('AddRestaurantSuppliers/', views.AddRestaurantSuppliers, name='AddRestaurantSuppliers'),
    path('UpdateRestaurantSuppliers/<int:id>/', views.UpdateRestaurantSuppliers, name='UpdateRestaurantSuppliers'),








    #-------------------GET HOTE  ORDER ITEMS-----------------
    path('ViewRestaurantOrderItemsPage/<int:id>/', views.ViewRestaurantOrderItemsPage, name='ViewRestaurantOrderItemsPage'),

    #-------------------GET HOTE DRINKS ORDER ITEMS-----------------
    path('ViewRestaurantDrinksOrderItemsPage/<int:id>/', views.ViewRestaurantDrinksOrderItemsPage, name='ViewRestaurantDrinksOrderItemsPage'),

   
]