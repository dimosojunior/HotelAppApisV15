from . import views
from django.urls import path


urlpatterns = [

	path(
        "request-password-reset/",
        views.PasswordReset.as_view(),
        name="request-password-reset",
    ),
    path(
        "password-reset/<str:encoded_pk>/<str:token>/",
        views.ResetPasswordAPI.as_view(),
        name="reset-password",
    ),

    path('register_user/', views.RegistrationView.as_view(), name='register'),
    path('login_user/', views.ReactLoginView.as_view(), name='login'),
    path('logout_user/', views.LogoutView.as_view(), name='logout'),
    path('user_data/', views.UserDataView.as_view(), name='user-data'),






    path('AdminHomePage/', views.AdminHomePage, name='AdminHomePage'),
    path('RegisterNewUserByAdmin/', views.RegisterNewUserByAdmin, name='RegisterNewUserByAdmin'),

]