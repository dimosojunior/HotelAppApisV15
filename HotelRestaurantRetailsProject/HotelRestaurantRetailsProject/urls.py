"""HotelRestaurantRetailsProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import TemplateView

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="HOTEL APP APIS",
        default_version='v1',
        description="A Rest API HOTEL APP",
        #terms_of_services="https://www.google.com/policies/terms",
        contact=openapi.Contact(email="juniordimoso8@gmail.com"),
        #license=openapi.License(name="BSD License"),
        ),
        public=True,
        permission_classes=[permissions.AllowAny],
    )


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('TemplatesApp.urls')),
    path('RestaurantApp/', include('RestaurantTemplatesApp.urls')),
    path('RetailsApp/', include('RetailsTemplatesApp.urls')),

    path('Hotel/', include('HotelApis.urls')),
    path('Account/', include('AccountApis.urls')),
    path('Restaurant/', include('RestaurantApis.urls')),
    path('Retails/', include('RetailsApis.urls')),
    path('Cart/', include('CartApis.urls')),
    path('PostData/', include('PostDataApp.urls')),


    path('accounts/', include('rest_framework.urls')),

    #urls for swagger documentation
    path('swagger<format>.json|.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/',schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
admin.site.site_header= "HOTEL APP PROJECT"
admin.site.site_title = "ADMIN AREA"
admin.site.index_title = "WELCOME TO ADMIN DASHBOARD"



if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

