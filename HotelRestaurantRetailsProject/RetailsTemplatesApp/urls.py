from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('RetailsHomePage/', views.RetailsHomePage, name='RetailsHomePage'),

    path('RetailsDeactivateUsersPage/', views.RetailsDeactivateUsersPage, name='RetailsDeactivateUsersPage'),
    path('Retailsdeactivate_inactive_users/', views.Retailsdeactivate_inactive_users, name='Retailsdeactivate_inactive_users'),

    path('Retails_search_username_UnpaidRetailsMyUser_autocomplete/', views.Retails_search_username_UnpaidRetailsMyUser_autocomplete, name='Retails_search_username_UnpaidRetailsMyUser_autocomplete'),
    path('Retails_search_email_UnpaidRetailsMyUser_autocomplete/', views.Retails_search_email_UnpaidRetailsMyUser_autocomplete, name='Retails_search_email_UnpaidRetailsMyUser_autocomplete'),
    path('Retails_search_company_name_UnpaidRetailsMyUser_autocomplete/', views.Retails_search_company_name_UnpaidRetailsMyUser_autocomplete, name='Retails_search_company_name_UnpaidRetailsMyUser_autocomplete'),
    path('UpdateUnpaidRetailsMyUser/<int:id>/', views.UpdateUnpaidRetailsMyUser, name='UpdateUnpaidRetailsMyUser'),




    path('RetailsactivateUsersPage/', views.RetailsactivateUsersPage, name='RetailsactivateUsersPage'),
    path('Retailsactivate_inactive_users/', views.Retailsactivate_inactive_users, name='Retailsactivate_inactive_users'),

    path('Retails_search_username_paidRetailsMyUser_autocomplete/', views.Retails_search_username_paidRetailsMyUser_autocomplete, name='Retails_search_username_paidRetailsMyUser_autocomplete'),
    path('Retails_search_email_paidRetailsMyUser_autocomplete/', views.Retails_search_email_paidRetailsMyUser_autocomplete, name='Retails_search_email_paidRetailsMyUser_autocomplete'),
    path('Retails_search_company_name_paidRetailsMyUser_autocomplete/', views.Retails_search_company_name_paidRetailsMyUser_autocomplete, name='Retails_search_company_name_paidRetailsMyUser_autocomplete'),
    path('UpdatepaidRetailsMyUser/<int:id>/', views.UpdatepaidRetailsMyUser, name='UpdatepaidRetailsMyUser'),


    path('RetailsSignupPage/', views.RetailsSignupPage, name='RetailsSignupPage'),
    path('RetailsUpdateUser/<int:id>/', views.RetailsUpdateUser, name='RetailsUpdateUser'),
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
    path('Retailschange_password/', views.RetailsPasswordChangeView.as_view(template_name = "Account/Retailspassword_change.html"), name="Retailschange-password"),


    # path('LogoutPage/', views.LogoutPage, name='LogoutPage'),





    #------------------ALL Retails USERS------------------------

    #path('AllUnpaidRetailsMyUserPage/', views.AllUnpaidRetailsMyUserPage, name='AllUnpaidRetailsMyUserPage'),




    path('RetailsCustomersPage/', views.RetailsCustomersPage, name='RetailsCustomersPage'),
    path('Retails_search_customer_autocomplete/', views.Retails_search_customer_autocomplete, name='Retails_search_customer_autocomplete'),
    path('Retails_search_address_autocomplete/', views.Retails_search_address_autocomplete, name='Retails_search_address_autocomplete'),
    path('DeleteRetailsCustomerPage/<int:id>/', views.DeleteRetailsCustomerPage, name='DeleteRetailsCustomerPage'),
    path('AddRetailsCustomerPage/', views.AddRetailsCustomerPage, name='AddRetailsCustomerPage'),
    path('UpdateRetailsCustomerPage/<int:id>/', views.UpdateRetailsCustomerPage, name='UpdateRetailsCustomerPage'),




    #---------------Retails BUSINESS UNIT-----------------------
    path('RetailsBusinessUnitPage/', views.RetailsBusinessUnitPage, name='RetailsBusinessUnitPage'),
    path('Retails_search_Code_Business_Unit_autocomplete/', views.Retails_search_Code_Business_Unit_autocomplete, name='Retails_search_Code_Business_Unit_autocomplete'),
    path('Retails_search_Description_Business_Unit_autocomplete/', views.Retails_search_Description_Business_Unit_autocomplete, name='Retails_search_Description_Business_Unit_autocomplete'),
    path('DeleteRetailsBusinessUnit/<int:id>/', views.DeleteRetailsBusinessUnit, name='DeleteRetailsBusinessUnit'),
    path('AddRetailsBusinessUnit/', views.AddRetailsBusinessUnit, name='AddRetailsBusinessUnit'),
    path('UpdateRetailsBusinessUnit/<int:id>/', views.UpdateRetailsBusinessUnit, name='UpdateRetailsBusinessUnit'),




    #---------------Retails LOCATION CODES-----------------------
    path('RetailsLocationCodePage/', views.RetailsLocationCodePage, name='RetailsLocationCodePage'),
    path('Retails_search_Code_Location_Code_autocomplete/', views.Retails_search_Code_Location_Code_autocomplete, name='Retails_search_Code_Location_Code_autocomplete'),
    path('Retails_search_Description_Location_Code_autocomplete/', views.Retails_search_Description_Location_Code_autocomplete, name='Retails_search_Description_Location_Code_autocomplete'),
    path('DeleteRetailsLocationCode/<int:id>/', views.DeleteRetailsLocationCode, name='DeleteRetailsLocationCode'),
    path('AddRetailsLocationCode/', views.AddRetailsLocationCode, name='AddRetailsLocationCode'),
    path('UpdateRetailsLocationCode/<int:id>/', views.UpdateRetailsLocationCode, name='UpdateRetailsLocationCode'),




    #---------------Retails PROCESS CONFIG-----------------------
    path('RetailsProcessConfigPage/', views.RetailsProcessConfigPage, name='RetailsProcessConfigPage'),
    path('Retails_search_ProcesId_process_config_autocomplete/', views.Retails_search_ProcesId_process_config_autocomplete, name='Retails_search_ProcesId_process_config_autocomplete'),
    path('Retails_search_Description_process_config_autocomplete/', views.Retails_search_Description_process_config_autocomplete, name='Retails_search_Description_process_config_autocomplete'),
    path('DeleteRetailsProcessConfig/<int:id>/', views.DeleteRetailsProcessConfig, name='DeleteRetailsProcessConfig'),
    path('AddRetailsProcessConfig/', views.AddRetailsProcessConfig, name='AddRetailsProcessConfig'),
    path('UpdateRetailsProcessConfig/<int:id>/', views.UpdateRetailsProcessConfig, name='UpdateRetailsProcessConfig'),


    #---------------Retails STORE CODES-----------------------
    path('RetailsStoreCodePage/', views.RetailsStoreCodePage, name='RetailsStoreCodePage'),
    path('Retails_search_Code_store_code_autocomplete/', views.Retails_search_Code_store_code_autocomplete, name='Retails_search_Code_store_code_autocomplete'),
    path('Retails_search_Description_store_code_autocomplete/', views.Retails_search_Description_store_code_autocomplete, name='Retails_search_Description_store_code_autocomplete'),
    path('DeleteRetailsStoreCode/<int:id>/', views.DeleteRetailsStoreCode, name='DeleteRetailsStoreCode'),
    path('AddRetailsStoreCode/', views.AddRetailsStoreCode, name='AddRetailsStoreCode'),
    path('UpdateRetailsStoreCode/<int:id>/', views.UpdateRetailsStoreCode, name='UpdateRetailsStoreCode'),




    #---------------Retails STORE BIN CODES-----------------------
    path('RetailsStoreBinCodePage/', views.RetailsStoreBinCodePage, name='RetailsStoreBinCodePage'),
    path('Retails_search_StoreBinCode_store_bin_code_autocomplete/', views.Retails_search_StoreBinCode_store_bin_code_autocomplete, name='Retails_search_StoreBinCode_store_bin_code_autocomplete'),
    path('Retails_search_CardNo_store_bin_code_autocomplete/', views.Retails_search_CardNo_store_bin_code_autocomplete, name='Retails_search_CardNo_store_bin_code_autocomplete'),
    path('Retails_search_Description_store_bin_code_autocomplete/', views.Retails_search_Description_store_bin_code_autocomplete, name='Retails_search_Description_store_bin_code_autocomplete'),
    path('DeleteRetailsStoreBinCode/<int:id>/', views.DeleteRetailsStoreBinCode, name='DeleteRetailsStoreBinCode'),
    path('AddRetailsStoreBinCode/', views.AddRetailsStoreBinCode, name='AddRetailsStoreBinCode'),
    path('UpdateRetailsStoreBinCode/<int:id>/', views.UpdateRetailsStoreBinCode, name='UpdateRetailsStoreBinCode'),



    #---------------Retails EVENT CODES-----------------------
    path('RetailsEventCodePage/', views.RetailsEventCodePage, name='RetailsEventCodePage'),
    path('Retails_search_Code_Event_Code_autocomplete/', views.Retails_search_Code_Event_Code_autocomplete, name='Retails_search_Code_Event_Code_autocomplete'),
    path('Retails_search_Description_Event_Code_autocomplete/', views.Retails_search_Description_Event_Code_autocomplete, name='Retails_search_Description_Event_Code_autocomplete'),
    path('DeleteRetailsEventCode/<int:id>/', views.DeleteRetailsEventCode, name='DeleteRetailsEventCode'),
    path('AddRetailsEventCode/', views.AddRetailsEventCode, name='AddRetailsEventCode'),
    path('UpdateRetailsEventCode/<int:id>/', views.UpdateRetailsEventCode, name='UpdateRetailsEventCode'),



    #---------------Retails EVENT ALERT-----------------------
    path('RetailsEventAlertPage/', views.RetailsEventAlertPage, name='RetailsEventAlertPage'),
    path('Retails_search_Code_AlertID_autocomplete/', views.Retails_search_Code_AlertID_autocomplete, name='Retails_search_Code_AlertID_autocomplete'),
    path('DeleteRetailsEventAlert/<int:id>/', views.DeleteRetailsEventAlert, name='DeleteRetailsEventAlert'),
    path('AddRetailsEventAlert/', views.AddRetailsEventAlert, name='AddRetailsEventAlert'),
    path('UpdateRetailsEventAlert/<int:id>/', views.UpdateRetailsEventAlert, name='UpdateRetailsEventAlert'),




    #---------------Retails UOM SHORT CODES-----------------------
    path('RetailsUOMPage/', views.RetailsUOMPage, name='RetailsUOMPage'),
    path('Retails_search_UOMShortCode_RetailsUOM_autocomplete/', views.Retails_search_UOMShortCode_RetailsUOM_autocomplete, name='Retails_search_UOMShortCode_RetailsUOM_autocomplete'),
    path('DeleteRetailsUOM/<int:id>/', views.DeleteRetailsUOM, name='DeleteRetailsUOM'),
    path('AddRetailsUOM/', views.AddRetailsUOM, name='AddRetailsUOM'),
    path('UpdateRetailsUOM/<int:id>/', views.UpdateRetailsUOM, name='UpdateRetailsUOM'),



    #---------------Retails UOM SHORT CODES-----------------------
    path('RetailsBOMPage/', views.RetailsBOMPage, name='RetailsBOMPage'),
    path('Retails_search_Code_RetailsBOM_autocomplete/', views.Retails_search_Code_RetailsBOM_autocomplete, name='Retails_search_Code_RetailsBOM_autocomplete'),
    path('Retails_search_Name_RetailsBOM_autocomplete/', views.Retails_search_Name_RetailsBOM_autocomplete, name='Retails_search_Name_RetailsBOM_autocomplete'),
    path('DeleteRetailsBOM/<int:id>/', views.DeleteRetailsBOM, name='DeleteRetailsBOM'),
    path('AddRetailsBOM/', views.AddRetailsBOM, name='AddRetailsBOM'),
    path('UpdateRetailsBOM/<int:id>/', views.UpdateRetailsBOM, name='UpdateRetailsBOM'),

    path('RetailsBOMDetailPage/', views.RetailsBOMDetailPage, name='RetailsBOMDetailPage'),
    path('AddRetailsBOMFiles/', views.AddRetailsBOMFiles, name='AddRetailsBOMFiles'),







    #-------------------HOTE L PRODUCTS CATEGORY----------------
    #-----All Categories----------
    path('RetailsProductsCategoriesPage/', views.RetailsProductsCategoriesPage, name='RetailsProductsCategoriesPage'),

    path('ViewRetailsCategoriesPage/<int:id>/', views.ViewRetailsCategoriesPage, name='ViewRetailsCategoriesPage'),
    path('UpdateRetailsCategories/<int:id>/', views.UpdateRetailsCategories, name='UpdateRetailsCategories'),
    path('DeleteRetailsCategories/<int:id>/', views.DeleteRetailsCategories, name='DeleteRetailsCategories'),


    #-------------------Retails DRINKS  PRODUCTS CATEGORIES-------------
    path('ViewRetailsDrinksCategoriesPage/<int:id>/', views.ViewRetailsDrinksCategoriesPage, name='ViewRetailsDrinksCategoriesPage'),
    path('UpdateRetailsDrinksCategories/<int:id>/', views.UpdateRetailsDrinksCategories, name='UpdateRetailsDrinksCategories'),
    path('DeleteRetailsDrinksCategories/<int:id>/', views.DeleteRetailsDrinksCategories, name='DeleteRetailsDrinksCategories'),



    








    #---------------------PRODUCTS ITSELF MAINTENANCE---------

    path('RetailsProductsPage/', views.RetailsProductsPage, name='RetailsProductsPage'),
    

    #-------------------- PRODUCTS-------------
    path('RetailsProductsPage/', views.RetailsProductsPage, name='RetailsProductsPage'),
    path('search_product_name_RetailsProducts_autocomplete/', views.search_product_name_RetailsProducts_autocomplete, name='search_product_name_RetailsProducts_autocomplete'),
    path('search_product_second_name_RetailsProducts_autocomplete/', views.search_product_second_name_RetailsProducts_autocomplete, name='search_product_second_name_RetailsProducts_autocomplete'),
    path('AddRetailsProducts/', views.AddRetailsProducts, name='AddRetailsProducts'),
    path('DeleteRetailsProducts/<int:id>/', views.DeleteRetailsProducts, name='DeleteRetailsProducts'),
    path('UpdateRetailsProducts/<int:id>/', views.UpdateRetailsProducts, name='UpdateRetailsProducts'),

    #--------------------DRINKS PRODUCTS-------------
    path('RetailsDrinksProductsPage/', views.RetailsDrinksProductsPage, name='RetailsDrinksProductsPage'),
    path('search_product_name_RetailsDrinksProducts_autocomplete/', views.search_product_name_RetailsDrinksProducts_autocomplete, name='search_product_name_RetailsDrinksProducts_autocomplete'),
    path('search_product_second_name_RetailsDrinksProducts_autocomplete/', views.search_product_second_name_RetailsDrinksProducts_autocomplete, name='search_product_second_name_RetailsDrinksProducts_autocomplete'),
    path('AddRetailsDrinksProducts/', views.AddRetailsDrinksProducts, name='AddRetailsDrinksProducts'),
    path('DeleteRetailsDrinksProducts/<int:id>/', views.DeleteRetailsDrinksProducts, name='DeleteRetailsDrinksProducts'),
    path('UpdateRetailsDrinksProducts/<int:id>/', views.UpdateRetailsDrinksProducts, name='UpdateRetailsDrinksProducts'),




    







    #----------------UPLOAD PRODUCTS----------------------------------------
    path('UploadRetailsProductsPage/', views.UploadRetailsProductsPage, name='UploadRetailsProductsPage'),
    
    path('UploadRetailsProductsPage/', views.UploadRetailsProductsPage, name='UploadRetailsProductsPage'),
    path('UploadRetailsDrinksProductsPage/', views.UploadRetailsDrinksProductsPage, name='UploadRetailsDrinksProductsPage'),
    





    #------------------------------ORDERS--------------------------------

    path('RetailsOrdersPage/', views.RetailsOrdersPage, name='RetailsOrdersPage'),

    #-------------Retails  ORDERS----------------------------------
    path('RetailsOrderPage/', views.RetailsOrderPage, name='RetailsOrderPage'),
    path('DeleteRetailsOrder/<int:id>/', views.DeleteRetailsOrder, name='DeleteRetailsOrder'),

    #-------------Retails Drinks ORDERS----------------------------------
    path('RetailsDrinksOrderPage/', views.RetailsDrinksOrderPage, name='RetailsDrinksOrderPage'),
    path('DeleteRetailsDrinksOrder/<int:id>/', views.DeleteRetailsDrinksOrder, name='DeleteRetailsDrinksOrder'),

    




    


    #------------------------STAFF MAINTENANCE_-----------------
    path('RetailsMyUserPage/', views.RetailsMyUserPage, name='RetailsMyUserPage'),
    path('Retails_search_username_RetailsMyUser_autocomplete/', views.Retails_search_username_RetailsMyUser_autocomplete, name='Retails_search_username_RetailsMyUser_autocomplete'),
    path('Retails_search_email_RetailsMyUser_autocomplete/', views.Retails_search_email_RetailsMyUser_autocomplete, name='Retails_search_email_RetailsMyUser_autocomplete'),
    path('DeleteRetailsMyUser/<int:id>/', views.DeleteRetailsMyUser, name='DeleteRetailsMyUser'),





    #--------------------Retails SUPPLIERS_------------------------

    path('RetailsSuppliersPage/', views.RetailsSuppliersPage, name='RetailsSuppliersPage'),
    path('Retails_search_SupplierFullName_RetailsSuppliers_autocomplete/', views.Retails_search_SupplierFullName_RetailsSuppliers_autocomplete, name='Retails_search_SupplierFullName_RetailsSuppliers_autocomplete'),
    path('Retails_search_Keyword_RetailsSuppliers_autocomplete/', views.Retails_search_Keyword_RetailsSuppliers_autocomplete, name='Retails_search_Keyword_RetailsSuppliers_autocomplete'),
    path('DeleteRetailsSuppliers/<int:id>/', views.DeleteRetailsSuppliers, name='DeleteRetailsSuppliers'),
    path('AddRetailsSuppliers/', views.AddRetailsSuppliers, name='AddRetailsSuppliers'),
    path('UpdateRetailsSuppliers/<int:id>/', views.UpdateRetailsSuppliers, name='UpdateRetailsSuppliers'),








    #-------------------GET HOTE  ORDER ITEMS-----------------
    path('ViewRetailsOrderItemsPage/<int:id>/', views.ViewRetailsOrderItemsPage, name='ViewRetailsOrderItemsPage'),

    #-------------------GET HOTE DRINKS ORDER ITEMS-----------------
    path('ViewRetailsDrinksOrderItemsPage/<int:id>/', views.ViewRetailsDrinksOrderItemsPage, name='ViewRetailsDrinksOrderItemsPage'),

   
]