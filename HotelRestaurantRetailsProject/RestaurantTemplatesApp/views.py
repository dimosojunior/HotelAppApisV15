from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect, reverse, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from HotelApis.models import *
from .models import *
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Sum, Max, Min, Avg
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView, View

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.db.models import Q
import datetime
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .forms import *
from django.contrib.auth.models import User, auth

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.auth.views import PasswordChangeView
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Sum
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect

from django.utils import timezone
from django.db.models import Sum, Max, Min, Avg


from .resources import *
from tablib import Dataset

import datetime

import csv
from .forms import *
from RestaurantApis.models import *

UserModel = get_user_model()


#tunadisplay users wote ambao wapo active lakini  hawajalipa yani
#bila kuweka paid status ili uweze kuwaadeactivate mmoja mmoja

@login_required(login_url='SigninPage')
def RestaurantDeactivateUsersPage(request):

    queryset = MyUser.objects.filter(
        #is_active=True,
        is_superuser=False,
        is_restaurant_user=True,
        is_paid=True

        ).order_by('-id')

    get_unpaid_sum = MyUser.objects.filter(
        #is_active=True,
        is_superuser=False,
        is_restaurant_user=True,
        is_paid=True
        ).count()


    form = UnpaidRestaurantMyUserSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            email = form.cleaned_data.get('email', '')
            username = form.cleaned_data.get('username', '')
            company_name = form.cleaned_data.get('company_name', '')

            # Use Q objects to construct the query
            query = Q()
            if email:
                query |= Q(email__icontains=email)
            if username:
                query |= Q(username__icontains=username)

            if company_name:
                query |= Q(company_name__icontains=company_name)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = MyUser.objects.filter(query)


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
        "get_unpaid_sum":get_unpaid_sum,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantDeactivateUsersPage.html', context)






@login_required(login_url='SigninPage')
def Restaurant_search_username_UnpaidRestaurantMyUser_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(username__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = MyUser.objects.filter(search)
    mylist= []
    mylist += [x.username for x in queryset]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Restaurant_search_email_UnpaidRestaurantMyUser_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(email__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = MyUser.objects.filter(search)
    mylist= []
    mylist += [x.email for x in queryset]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def Restaurant_search_company_name_UnpaidRestaurantMyUser_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(company_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = MyUser.objects.filter(search)
    mylist= []
    mylist += [x.company_name for x in queryset]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def UpdateUnpaidRestaurantMyUser(request,id):
    x = MyUser.objects.get(id=id)
    form = UpdateUnpaidRestaurantMyUserForm(instance=x)
    
    if request.method == "POST":
        form=UpdateUnpaidRestaurantMyUserForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()


            subject = "Your account has been deactivated"
            message = "Your account has been deactivated "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [x.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantDeactivateUsersPage')

        messages.success(request,f"Fail to update data")
        return redirect('UpdateUnpaidRestaurantMyUser', id=id)

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateUnpaidRestaurantMyUser.html', context)












#tunawadisplay users wote ambao accunt zao zipo inactive ili twweze
#kuwaactivate mmoja mmoja, ila paid ni False ili tuweze kuona wote ambao
#ccount zao zilikuwa deactivated then tuziactivate
@login_required(login_url='SigninPage')
def RestaurantactivateUsersPage(request):

    queryset = MyUser.objects.filter(
        #is_active=False,
        is_superuser=False,
        is_restaurant_user=True,
        is_paid=False

        ).order_by('-id')

    get_paid_sum = MyUser.objects.filter(
        #is_active=False,
        is_superuser=False,
        is_restaurant_user=True,
        is_paid=False
        ).count()


    form = paidRestaurantMyUserSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            email = form.cleaned_data.get('email', '')
            username = form.cleaned_data.get('username', '')
            company_name = form.cleaned_data.get('company_name', '')

            # Use Q objects to construct the query
            query = Q()
            if email:
                query |= Q(email__icontains=email)
            if username:
                query |= Q(username__icontains=username)

            if company_name:
                query |= Q(company_name__icontains=company_name)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = MyUser.objects.filter(query)


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
        "get_paid_sum":get_paid_sum,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantactivateUsersPage.html',context)






@login_required(login_url='SigninPage')
def Restaurant_search_username_paidRestaurantMyUser_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(username__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = MyUser.objects.filter(search)
    mylist= []
    mylist += [x.username for x in queryset]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Restaurant_search_email_paidRestaurantMyUser_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(email__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = MyUser.objects.filter(search)
    mylist= []
    mylist += [x.email for x in queryset]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def Restaurant_search_company_name_paidRestaurantMyUser_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(company_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = MyUser.objects.filter(search)
    mylist= []
    mylist += [x.company_name for x in queryset]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def UpdatepaidRestaurantMyUser(request,id):
    x = MyUser.objects.get(id=id)
    form = UpdatepaidRestaurantMyUserForm(instance=x)
    
    if request.method == "POST":
        form=UpdatepaidRestaurantMyUserForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()


            subject = "Your account has been activated"
            message = "Your account has been activated "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [x.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantactivateUsersPage')

        messages.success(request,f"Fail to update data")
        return redirect('UpdatepaidRestaurantMyUser', id=id)

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdatepaidRestaurantMyUser.html', context)









@login_required(login_url='SigninPage')
def RestaurantHomePage(request):

    return render(request, 'RestaurantTemplatesApp/Restauranthome.html')


#hapa tunafungiwa wote kwa pamoja ambao account zao zipo active 
#lakini hawajalipa
@login_required(login_url='SigninPage')
def Restaurantdeactivate_inactive_users(request):
    # Get the current date
    current_date = timezone.now()
    # Calculate the date threshold (1 days ago)
    threshold_date = current_date - timezone.timedelta(days=1)

    # Get all users whose registration date is older than 1 days
    users_to_deactivate = MyUser.objects.filter(
        date_joined__lt=threshold_date, 
        #is_active=True,
        is_superuser=False,
        is_restaurant_user=True,
        is_paid=True
        )

    # Update the is_active field and send emails
    for user in users_to_deactivate:
        user.is_active = False
        user.is_paid = False
        user.save()

        # Send an email to the user
        subject = "Your account has been deactivated"
        message = "Your account has been deactivated because it has been inactive for more than 1 days."
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

    messages.success(request, f"{len(users_to_deactivate)} users were deactivated.")
    return redirect("RestaurantDeactivateUsersPage")


#hapa tunawaactivate wote kwa pamoja ambao account zao zipo inactive 
#lakini wamelipa
@login_required(login_url='SigninPage')
def Restaurantactivate_inactive_users(request):
    # Get the current date
    current_date = timezone.now()
    # Calculate the date threshold (1 days ago)
    threshold_date = current_date - timezone.timedelta(days=1)

    # Get all users whose registration date is older than 1 days
    users_to_deactivate = MyUser.objects.filter(
        date_joined__lt=threshold_date, 
        #is_active=False ,
        is_superuser = False,
        is_restaurant_user=True,
        is_paid=False
        )

    # Update the is_active field and send emails
    for user in users_to_deactivate:
        user.is_active = True
        user.is_paid = True
        user.save()

        # Send an email to the user
        subject = "Your account has been activated"
        message = "Your account has been activated now"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

    messages.success(request, f"{len(users_to_deactivate)} users were activated.")
    return redirect("RestaurantactivateUsersPage")





def RestaurantSignupPage(request):
    if request.method == "POST":
        form = MyUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserCodes = request.POST.get('UserCodes')
            email = request.POST.get('email')
            username = request.POST.get('username')

            
            subject = f"Hey {username} this is your SCI Code that youcan use to login in our system"
            #message = f"Ahsante  {username} kwa kujisajili kwenye mfumo wetu kama {username} email yako {email}. Nunua bidhaa bora na kwa bei nafuu kupitia Dimoso Electronics Center, unaweza kuweka order au kunitumia email kwa ajili ya kupata bidhaa zako kwa haraka. Ahsante {username} endelea kutembelea mfumo wetu "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, UserCodes, from_email, recipient_list, fail_silently=True)

            messages.success(request, f'{user.username} is registered successfully')
            return redirect('RestaurantSignupPage')
    else:
        form = MyUserForm()

    context = {
        "form": form
    }
    return render(request, 'Account/RestaurantSignupPage.html', context)





# def SigninPage(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         UserCodes = request.POST.get('UserCodes')

#         # Use Django's authenticate function to check email and password
#         user = authenticate(request, email=email, password=password)

#         if user is not None:
#             # Check if UserCodes matches the user's UserCodes
#             if user.UserCodes == UserCodes:
#                 login(request, user)
#                 return redirect('HomePage')
#             else:
#                 messages.info(request, 'Invalid User Codes')
#                 return redirect('SigninPage')
#         else:
#             messages.info(request, 'Credentials Invalid')
#             return redirect('SigninPage')
#     else:
#         return render(request, 'Account/SigninPage.html')




# @login_required(login_url='SigninPage')
# def LogoutPage(request):
#     auth.logout(request)
#     return redirect('SigninPage')




class RestaurantPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    #login_url = 'login'
    success_url = reverse_lazy('RestaurantHomePage')




@login_required(login_url='SigninPage')
def RestaurantUpdateUser(request, id):
    x = MyUser.objects.get(id=id)
    if request.method == "POST":
        form = UpdateMyUserForm(request.POST, instance=x)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'{x.username} is updated successfully')
            return redirect('RestaurantUpdateUser',id=id)
    else:
        form = UpdateMyUserForm(instance=x)

    context = {
        "form": form
    }
    return render(request, 'Account/RestaurantUpdateUser.html', context)










































#-------------------CUSTOMERS--------------------------------



@login_required(login_url='SigninPage')
def RestaurantCustomersPage(request):
    customers = RestaurantCustomers.objects.all().order_by('-id')
    form = RestaurantCustomersSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            customer_full_name = form.cleaned_data.get('CustomerFullName', '')
            customer_address = form.cleaned_data.get('CustomerAddress', '')

            # Use Q objects to construct the query
            query = Q()
            if customer_full_name:
                query |= Q(CustomerFullName__icontains=customer_full_name)
            if customer_address:
                query |= Q(CustomerAddress__icontains=customer_address)

            customers = RestaurantCustomers.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(customers,5)
    page = request.GET.get('page')
    try:
        customers=paginator.page(page)
    except PageNotAnInteger:
        customers=paginator.page(1)
    except EmptyPage:
        customers=paginator.page(paginator.num_pages)

    context = {
        "customers": customers,
        "form": form,
        "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantCustomersPage.html', context)





@login_required(login_url='SigninPage')
def Restaurant_search_customer_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CustomerFullName__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    customers = RestaurantCustomers.objects.filter(search)
    mylist= []
    mylist += [x.CustomerFullName for x in customers]
    return JsonResponse(mylist, safe=False)

def Restaurant_search_address_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CustomerAddress__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    customers = RestaurantCustomers.objects.filter(search)
    mylist= []
    mylist += [x.CustomerAddress for x in customers]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def DeleteRestaurantCustomerPage(request,id):
    x = RestaurantCustomers.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"{x.CustomerFullName} was deleted Successfully")
    return redirect('RestaurantCustomersPage')
    



@login_required(login_url='SigninPage')
def AddRestaurantCustomerPage(request):
    
    form = AddRestaurantCustomerForm()
    
    if request.method == "POST":
        form=AddRestaurantCustomerForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantCustomersPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantCustomerPage')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantCustomerPage.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantCustomerPage(request,id):
    x = RestaurantCustomers.objects.get(id=id)
    form = AddRestaurantCustomerForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantCustomerForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"{x.CustomerFullName}   updated Successfully")
            return redirect('RestaurantCustomersPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantCustomerPage.html', context)






#---------------BUSINESS UNIT--------------------

@login_required(login_url='SigninPage')
def RestaurantBusinessUnitPage(request):
    queryset = RestaurantBusinessUnit.objects.all().order_by('-id')
    form = RestaurantBusinessUnitSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Description:
                query |= Q(Description__icontains=Description)

            queryset = RestaurantBusinessUnit.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantBusinessUnitPage.html', context)





@login_required(login_url='SigninPage')
def Restaurant_search_Code_Business_Unit_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantBusinessUnit.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Restaurant_search_Description_Business_Unit_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantBusinessUnit.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantBusinessUnit(request,id):
    x = RestaurantBusinessUnit.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Business Unit with code {x.Code} was deleted Successfully")
    return redirect('RestaurantBusinessUnitPage')
    

    


@login_required(login_url='SigninPage')
def AddRestaurantBusinessUnit(request):
    
    form = AddRestaurantBusinessUnitForm()
    
    if request.method == "POST":
        form=AddRestaurantBusinessUnitForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantBusinessUnitPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantBusinessUnit')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantBusinessUnit.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantBusinessUnit(request,id):
    x = RestaurantBusinessUnit.objects.get(id=id)
    form = AddRestaurantBusinessUnitForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantBusinessUnitForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantBusinessUnitPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantBusinessUnit.html', context)





















#---------------LOCATION CODE UNIT--------------------

@login_required(login_url='SigninPage')
def RestaurantLocationCodePage(request):
    queryset = RestaurantLocationCode.objects.all().order_by('-id')
    form = RestaurantLocationCodeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Description:
                query |= Q(Description__icontains=Description)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = RestaurantLocationCode.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }



    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            BusinessUnit = form['BusinessUnit'].value()

            

                                            
            queryset = RestaurantLocationCode.objects.filter(
                                            Code__icontains=form['Code'].value(),
                                            Description__icontains=form['Description'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (BusinessUnit != ''):
                queryset = RestaurantLocationCode.objects.all()
                queryset = queryset.filter(BusinessUnit_id=BusinessUnit)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantLocationCodePage.html', context)





@login_required(login_url='SigninPage')
def Restaurant_search_Code_Location_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantLocationCode.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Restaurant_search_Description_Location_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantLocationCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantLocationCode(request,id):
    x = RestaurantLocationCode.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Business Unit with code {x.Code} was deleted Successfully")
    return redirect('RestaurantLocationCodePage')
    

    


@login_required(login_url='SigninPage')
def AddRestaurantLocationCode(request):
    
    form = AddRestaurantLocationCodeForm()
    
    if request.method == "POST":
        form=AddRestaurantLocationCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantLocationCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantLocationCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantLocationCode.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantLocationCode(request,id):
    x = RestaurantLocationCode.objects.get(id=id)
    form = AddRestaurantLocationCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantLocationCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantLocationCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantLocationCode.html', context)












#----------------------Restaurant PROCESS CONFIG-----------------------




@login_required(login_url='SigninPage')
def RestaurantProcessConfigPage(request):
    queryset = RestaurantProcessConfig.objects.all().order_by('-id')
    form = RestaurantProcessConfigSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            ProcesId = form.cleaned_data.get('ProcesId', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if ProcesId:
                query |= Q(ProcesId__icontains=ProcesId)
            if Description:
                query |= Q(Description__icontains=Description)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = RestaurantProcessConfig.objects.filter(query)


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    

    return render(request, 'RestaurantTemplatesApp/RestaurantProcessConfigPage.html', context)





@login_required(login_url='SigninPage')
def Restaurant_search_ProcesId_process_config_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(ProcesId__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantProcessConfig.objects.filter(search)
    mylist= []
    mylist += [x.ProcesId for x in filters]
    return JsonResponse(mylist, safe=False)

def Restaurant_search_Description_process_config_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantProcessConfig.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantProcessConfig(request,id):
    x = RestaurantProcessConfig.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data deleted Successfully")
    return redirect('RestaurantProcessConfigPage')
    

    


@login_required(login_url='SigninPage')
def AddRestaurantProcessConfig(request):
    
    form = AddRestaurantProcessConfigForm()
    
    if request.method == "POST":
        form=AddRestaurantProcessConfigForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantProcessConfigPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantProcessConfig')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantProcessConfig.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantProcessConfig(request,id):
    x = RestaurantProcessConfig.objects.get(id=id)
    form = AddRestaurantProcessConfigForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantProcessConfigForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantProcessConfigPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantProcessConfig.html', context)





















#---------------Restaurant STORE CODE--------------------

@login_required(login_url='SigninPage')
def RestaurantStoreCodePage(request):
    queryset = RestaurantStoreCode.objects.all().order_by('-id')
    form = RestaurantStoreCodeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Description:
                query |= Q(Description__icontains=Description)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = RestaurantStoreCode.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }



    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            Location = form['Location'].value()
            Process = form['Process'].value()


            

                                            
            queryset = RestaurantStoreCode.objects.filter(
                                            Code__icontains=form['Code'].value(),
                                            Description__icontains=form['Description'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (Location != ''):
                queryset = RestaurantStoreCode.objects.all()
                queryset = queryset.filter(Location_id=Location)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

            if (Process != ''):
                queryset = RestaurantStoreCode.objects.all()
                queryset = queryset.filter(Process_id=Process)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }




    # if request.method == "POST":
    #     #kwa ajili ya kufilter items and category ktk form
            
    #         #category__icontains=form['category'].value(),
    #         Process = form['Process'].value()

            

                                            
    #         queryset = HotelStoreCode.objects.filter(
    #                                         Code__icontains=form['Code'].value(),
    #                                         Description__icontains=form['Description'].value()
    #                                         #last_updated__gte=form['start_date'].value(),
    #                                         # last_updated__lte=form['end_date'].value()
    #                                         #last_updated__range=[
    #                                             #form['start_date'].value(),
    #                                             #form['end_date'].value()
    #                                         #]
    #             )
    #         if (Process != ''):
    #             queryset = HotelStoreCode.objects.all()
    #             queryset = queryset.filter(Process_id=Process)

    #             #To SET  PAGINATION IN STOCK LIST PAGE
    #             paginator = Paginator(queryset,5)
    #             page = request.GET.get('page')
    #             try:
    #                 queryset=paginator.page(page)
    #             except PageNotAnInteger:
    #                 queryset=paginator.page(1)
    #             except EmptyPage:
    #                 queryset=paginator.page(paginator.num_pages)

    # context = {
    #     "queryset": queryset,
    #     "form": form,
    #     "page":page,
    # }

    return render(request, 'RestaurantTemplatesApp/RestaurantStoreCodePage.html', context)

    





@login_required(login_url='SigninPage')
def Restaurant_search_Code_store_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantStoreCode.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Restaurant_search_Description_store_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantStoreCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantStoreCode(request,id):
    x = RestaurantStoreCode.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data {x.Code} was deleted Successfully")
    return redirect('RestaurantStoreCodePage')
    

    


@login_required(login_url='SigninPage')
def AddRestaurantStoreCode(request):
    
    form = AddRestaurantStoreCodeForm()
    
    if request.method == "POST":
        form=AddRestaurantStoreCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantStoreCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantStoreCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantStoreCode.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantStoreCode(request,id):
    x = RestaurantStoreCode.objects.get(id=id)
    form = AddRestaurantStoreCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantStoreCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantStoreCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantStoreCode.html', context)
















#----------------------Restaurant STORE BIN CODE-----------------------




@login_required(login_url='SigninPage')
def RestaurantStoreBinCodePage(request):
    queryset = RestaurantStoreBinCode.objects.all().order_by('-id')
    form = RestaurantStoreBinCodeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            StoreBinCode = form.cleaned_data.get('StoreBinCode', '')
            Description = form.cleaned_data.get('Description', '')
            CardNo = form.cleaned_data.get('CardNo', '')

            # Use Q objects to construct the query
            query = Q()
            if StoreBinCode:
                query |= Q(StoreBinCode__icontains=StoreBinCode)
            if Description:
                query |= Q(Description__icontains=Description)

            if CardNo:
                query |= Q(CardNo__icontains=CardNo)

            
                #ZINAISHIA HAPA ZA KUSEARCH ILA CONTEXT IPO KWA CHINI

            queryset = RestaurantStoreBinCode.objects.filter(query)


    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    

    return render(request, 'RestaurantTemplatesApp/RestaurantStoreBinCodePage.html', context)





@login_required(login_url='SigninPage')
def Restaurant_search_StoreBinCode_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(StoreBinCode__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.StoreBinCode for x in filters]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Restaurant_search_CardNo_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CardNo__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.CardNo for x in filters]
    return JsonResponse(mylist, safe=False)


def Restaurant_search_Description_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantStoreBinCode(request,id):
    x = RestaurantStoreBinCode.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data deleted Successfully")
    return redirect('RestaurantStoreBinCodePage')
    

    


@login_required(login_url='SigninPage')
def AddRestaurantStoreBinCode(request):
    
    form = AddRestaurantStoreBinCodeForm()
    
    if request.method == "POST":
        form=AddRestaurantStoreBinCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantStoreBinCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantStoreBinCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantStoreBinCode.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantStoreBinCode(request,id):
    x = RestaurantStoreBinCode.objects.get(id=id)
    form = AddRestaurantStoreBinCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantStoreBinCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantStoreBinCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantStoreBinCode.html', context)















#-------------------------EVENT CODES---------------------------


@login_required(login_url='SigninPage')
def RestaurantEventCodePage(request):
    queryset = RestaurantEventCode.objects.all().order_by('-id')
    form = RestaurantEventCodeSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Description = form.cleaned_data.get('Description', '')

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Description:
                query |= Q(Description__icontains=Description)

            queryset = RestaurantEventCode.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantEventCodePage.html', context)





@login_required(login_url='SigninPage')
def Restaurant_search_Code_Event_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantEventCode.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Restaurant_search_Description_Event_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantEventCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantEventCode(request,id):
    x = RestaurantEventCode.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RestaurantEventCodePage')
    

    


@login_required(login_url='SigninPage')
def AddRestaurantEventCode(request):
    
    form = AddRestaurantEventCodeForm()
    
    if request.method == "POST":
        form=AddRestaurantEventCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantEventCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantEventCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantEventCode.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantEventCode(request,id):
    x = RestaurantEventCode.objects.get(id=id)
    form = AddRestaurantEventCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantEventCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantEventCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantEventCode.html', context)
















#-----------------Restaurant EVENT ALERT---------------------

@login_required(login_url='SigninPage')
def RestaurantEventAlertPage(request):
    queryset = RestaurantEventAlert.objects.all().order_by('-id')
    form = RestaurantEventAlertSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            AlertID = form.cleaned_data.get('AlertID', '')
            

            # Use Q objects to construct the query
            query = Q()
            if AlertID:
                query |= Q(AlertID__icontains=AlertID)
            

            queryset = RestaurantEventAlert.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantEventAlertPage.html', context)





@login_required(login_url='SigninPage')
def Restaurant_search_Code_AlertID_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(AlertID__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantEventAlert.objects.filter(search)
    mylist= []
    mylist += [x.AlertID for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantEventAlert(request,id):
    x = RestaurantEventAlert.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RestaurantEventAlertPage')
    

    


@login_required(login_url='SigninPage')
def AddRestaurantEventAlert(request):
    
    form = AddRestaurantEventAlertForm()
    
    if request.method == "POST":


        form=AddRestaurantEventAlertForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            ReceivedBy = request.POST.get('ReceivedBy')
            Message = request.POST.get('Message')

            
            subject = "Alert From Track-Sol"
            #message = f"Ahsante  {username} kwa kujisajili kwenye mfumo wetu kama {username} email yako {email}. Nunua bidhaa bora na kwa bei nafuu kupitia Dimoso Electronics Center, unaweza kuweka order au kunitumia email kwa ajili ya kupata bidhaa zako kwa haraka. Ahsante {username} endelea kutembelea mfumo wetu "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [ReceivedBy]
            send_mail(subject, Message, from_email, recipient_list, fail_silently=True)

            messages.success(request,f"Alert Added Successfully")
            return redirect('RestaurantEventAlertPage')

        messages.success(request,f"Failed to add new alert")
        return redirect('AddRestaurantEventAlert')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantEventAlert.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantEventAlert(request,id):
    x = RestaurantEventAlert.objects.get(id=id)
    form = AddRestaurantEventAlertForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantEventAlertForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Alert updated Successfully")
            return redirect('RestaurantEventAlertPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantEventAlert.html', context)












#---------------UOM SHORT CODES--------------------

@login_required(login_url='SigninPage')
def RestaurantUOMPage(request):
    queryset = RestaurantUOM.objects.all().order_by('-id')
    form = RestaurantUOMSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            UOMShortCode = form.cleaned_data.get('UOMShortCode', '')
            

            # Use Q objects to construct the query
            query = Q()
            if UOMShortCode:
                query |= Q(UOMShortCode__icontains=UOMShortCode)
            

            queryset = RestaurantUOM.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantUOMPage.html', context)





@login_required(login_url='SigninPage')
def Restaurant_search_UOMShortCode_RestaurantUOM_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(UOMShortCode__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantUOM.objects.filter(search)
    mylist= []
    mylist += [x.UOMShortCode for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantUOM(request,id):
    x = RestaurantUOM.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RestaurantUOMPage')
    

    


@login_required(login_url='SigninPage')
def AddRestaurantUOM(request):
    
    form = AddRestaurantUOMForm()
    
    if request.method == "POST":
        form=AddRestaurantUOMForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantUOMPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantUOM')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantUOM.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantUOM(request,id):
    x = RestaurantUOM.objects.get(id=id)
    form = AddRestaurantUOMForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantUOMForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantUOMPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantUOM.html', context)















#---------------BOM SHORT CODES--------------------

@login_required(login_url='SigninPage')
def RestaurantBOMPage(request):
    queryset = RestaurantBOM.objects.all().order_by('-id')
    form = RestaurantBOMSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Name = form.cleaned_data.get('Name', '')

            

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Name:
                query |= Q(Name__icontains=Name)
            

            queryset = RestaurantBOM.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantBOMPage.html', context)





@login_required(login_url='SigninPage')
def Restaurant_search_Code_RestaurantBOM_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantBOM.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Restaurant_search_Name_RestaurantBOM_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantBOM.objects.filter(search)
    mylist= []
    mylist += [x.Name for x in filters]
    return JsonResponse(mylist, safe=False)




@login_required(login_url='SigninPage')
def DeleteRestaurantBOM(request,id):
    x = RestaurantBOM.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RestaurantBOMPage')
    

    


@login_required(login_url='SigninPage')
def AddRestaurantBOM(request):
    
    form = AddRestaurantBOMForm()
    
    if request.method == "POST":
        form=AddRestaurantBOMForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantBOMPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantBOM')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantBOM.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantBOM(request,id):
    x = RestaurantBOM.objects.get(id=id)
    form = AddRestaurantBOMForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantBOMForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantBOMPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantBOM.html', context)







#----------------BOM DETAIL PAGE--------------------
@login_required(login_url='SigninPage')
def RestaurantBOMDetailPage(request):
    queryset = RestaurantBOM.objects.all().order_by('-id')
    form = RestaurantBOMSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            Code = form.cleaned_data.get('Code', '')
            Name = form.cleaned_data.get('Name', '')

            

            # Use Q objects to construct the query
            query = Q()
            if Code:
                query |= Q(Code__icontains=Code)
            if Name:
                query |= Q(Name__icontains=Name)
            

            queryset = RestaurantBOM.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantBOMDetailPage.html', context)










#------------BOM UPLOAD FILE----------------------------

@login_required(login_url='SigninPage')
def AddRestaurantBOMFiles(request):
    
    form = AddRestaurantBOMFilesForm()
    
    if request.method == "POST":
        form=AddRestaurantBOMFilesForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"File Uploaded Successfully")
            return redirect('AddRestaurantBOMFiles')

        messages.success(request,f"Failed to add upload file")
        return redirect('AddRestaurantBOMFiles')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantBOMFiles.html', context)




























#----------------------SALES& DISTRIBUTION-----------------



#------------PRODUCTS CATEGORIES----------------------------

@login_required(login_url='SigninPage')
def RestaurantProductsCategoriesPage(request):
    food = RestaurantCategories.objects.all().order_by('-id')
    drinks = RestaurantDrinksCategories.objects.all().order_by('-id')
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    # paginator = Paginator(food,5)
    # page = request.GET.get('page')
    # try:
    #     food=paginator.page(page)
    # except PageNotAnInteger:
    #     food=paginator.page(1)
    # except EmptyPage:
    #     food=paginator.page(paginator.num_pages)

    context = {
        "food": food,
        "drinks": drinks,
        
        # "form": form,
        # "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantProductsCategoriesPage.html', context)











#--------------------FOOD PRODUCTS CATEGORIES-------------------


#---------------------VIEW FOOD PRODUCT CATEGORY------------------
@login_required(login_url='SigninPage')
def ViewRestaurantCategoriesPage(request,id):
    queryset = RestaurantCategories.objects.get(id=id)

    form = AddRestaurantCategoriesForm()
    
    if request.method == "POST":
        form=AddRestaurantCategoriesForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data added successfully")
            return redirect('RestaurantProductsCategoriesPage')

        messages.success(request,f"Failed to add new data")
        return redirect('ViewRestaurantCategoriesPage',id=id)

    context = {
        "queryset": queryset,
        "form":form,
        
    }

    return render(request, 'ViewPages/ViewRestaurantCategoriesPage.html', context)



#------------UPDATE FOOD PRODUCTS CATEGORIES--------------
@login_required(login_url='SigninPage')
def UpdateRestaurantCategories(request,id):
    x = RestaurantCategories.objects.get(id=id)
    form = AddRestaurantCategoriesForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantCategoriesForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('ViewRestaurantCategoriesPage',id=id)

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantCategories.html', context)



@login_required(login_url='SigninPage')
def DeleteRestaurantCategories(request,id):
    x = RestaurantCategories.objects.get(id=id)

    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RestaurantProductsCategoriesPage')
    















#--------------------Drinks PRODUCTS CATEGORIES-------------------


#---------------------VIEW Drinks PRODUCT CATEGORY------------------
@login_required(login_url='SigninPage')
def ViewRestaurantDrinksCategoriesPage(request,id):
    queryset = RestaurantDrinksCategories.objects.get(id=id)

    form = AddRestaurantDrinksCategoriesForm()
    
    if request.method == "POST":
        form=AddRestaurantDrinksCategoriesForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data added successfully")
            return redirect('RestaurantProductsCategoriesPage')

        messages.success(request,f"Failed to add new data")
        return redirect('ViewRestaurantDrinksCategoriesPage',id=id)

    context = {
        "queryset": queryset,
        "form":form,
        
    }

    return render(request, 'ViewPages/ViewRestaurantDrinksCategoriesPage.html', context)



#------------UPDATE Drinks PRODUCTS CATEGORIES--------------
@login_required(login_url='SigninPage')
def UpdateRestaurantDrinksCategories(request,id):
    x = RestaurantDrinksCategories.objects.get(id=id)
    form = AddRestaurantDrinksCategoriesForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantDrinksCategoriesForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('ViewRestaurantDrinksCategoriesPage',id=id)

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantDrinksCategories.html', context)



@login_required(login_url='SigninPage')
def DeleteRestaurantDrinksCategories(request,id):
    x = RestaurantDrinksCategories.objects.get(id=id)

    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RestaurantProductsCategoriesPage')
































#-------------MAINTENANCE OF PRODUCTS ITSELF------------------



@login_required(login_url='SigninPage')
def RestaurantProductsPage(request):
    

    return render(request, 'RestaurantTemplatesApp/RestaurantProductsPage.html')




#-------------------FOOD PRODUCTS-------------------------

@login_required(login_url='SigninPage')
def RestaurantProductsPage(request):
    queryset = RestaurantProducts.objects.all().order_by('-id')

    form = RestaurantProductsSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            product_name = form.cleaned_data.get('product_name', '')
            product_second_name = form.cleaned_data.get('product_second_name', '')

            

            # Use Q objects to construct the query
            query = Q()
            if product_name:
                query |= Q(product_name__icontains=product_name)
            if product_second_name:
                query |= Q(product_second_name__icontains=product_second_name)
            

            queryset = RestaurantProducts.objects.filter(query)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }


    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            productCategory = form['productCategory'].value()

            

                                            
            queryset = RestaurantProducts.objects.filter(
                                            product_name__icontains=form['product_name'].value(),
                                            product_second_name__icontains=form['product_second_name'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (productCategory != ''):
                queryset = RestaurantProducts.objects.all().order_by('-id')
                queryset = queryset.filter(productCategory_id=productCategory)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantProductsPage.html', context)

@login_required(login_url='SigninPage')
def search_product_name_RestaurantProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_name for x in filters]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def search_product_second_name_RestaurantProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_second_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_second_name for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantProducts(request,id):
    x = RestaurantProducts.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RestaurantProductsPage')
    



@login_required(login_url='SigninPage')
def AddRestaurantProducts(request):
    
    form = AddRestaurantProductsForm()
    
    if request.method == "POST":
        form=AddRestaurantProductsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantProductsPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantProducts')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantProducts.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantProducts(request,id):
    x = RestaurantProducts.objects.get(id=id)
    form = AddRestaurantProductsForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantProductsForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantProductsPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantProducts.html', context)


























#-------------------DRINKS PRODUCTS-------------------------

@login_required(login_url='SigninPage')
def RestaurantDrinksProductsPage(request):
    queryset = RestaurantDrinksProducts.objects.all().order_by('-id')

    form = RestaurantDrinksProductsSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            product_name = form.cleaned_data.get('product_name', '')
            product_second_name = form.cleaned_data.get('product_second_name', '')

            

            # Use Q objects to construct the query
            query = Q()
            if product_name:
                query |= Q(product_name__icontains=product_name)
            if product_second_name:
                query |= Q(product_second_name__icontains=product_second_name)
            

            queryset = RestaurantDrinksProducts.objects.filter(query)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
            #category__icontains=form['category'].value(),
            productCategory = form['productCategory'].value()

            

                                            
            queryset = RestaurantDrinksProducts.objects.filter(
                                            product_name__icontains=form['product_name'].value(),
                                            product_second_name__icontains=form['product_second_name'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            if (productCategory != ''):
                queryset = RestaurantDrinksProducts.objects.all().order_by('-id')
                queryset = queryset.filter(productCategory_id=productCategory)

                #To SET  PAGINATION IN STOCK LIST PAGE
                paginator = Paginator(queryset,5)
                page = request.GET.get('page')
                try:
                    queryset=paginator.page(page)
                except PageNotAnInteger:
                    queryset=paginator.page(1)
                except EmptyPage:
                    queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantDrinksProductsPage.html', context)

@login_required(login_url='SigninPage')
def search_product_name_RestaurantDrinksProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantDrinksProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_name for x in filters]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def search_product_second_name_RestaurantDrinksProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_second_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RestaurantDrinksProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_second_name for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantDrinksProducts(request,id):
    x = RestaurantDrinksProducts.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RestaurantDrinksProductsPage')
    



@login_required(login_url='SigninPage')
def AddRestaurantDrinksProducts(request):
    
    form = AddRestaurantDrinksProductsForm()
    
    if request.method == "POST":
        form=AddRestaurantDrinksProductsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantDrinksProductsPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantDrinksProducts')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantDrinksProducts.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantDrinksProducts(request,id):
    x = RestaurantDrinksProducts.objects.get(id=id)
    form = AddRestaurantDrinksProductsForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantDrinksProductsForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantDrinksProductsPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantDrinksProducts.html', context)













































@login_required(login_url='SigninPage')
def UploadRestaurantProductsPage(request):
    

    return render(request, 'RestaurantTemplatesApp/UploadRestaurantProductsPage.html')





# @login_required(login_url='SigninPage')
# def UploadRestaurantProductsPage(request):
    
#     form = UploadRestaurantProductsForm()
    
#     if request.method == "POST":
#         form=UploadRestaurantProductsForm(request.POST or None, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request,f"File Uploaded Successfully")
#             return redirect('UploadRestaurantProductsPage')

#         messages.success(request,f"Failed to add upload file")
#         return redirect('UploadRestaurantProductsPage')


#     context = {
#         "form":form,
        

#     }
    
#     return render(request, 'RestaurantAddPage/UploadRestaurantProductsPage.html', context)



# @login_required(login_url='SigninPage')
# def UploadRestaurantDrinksProductsPage(request):
    
#     form = UploadRestaurantDrinksProductsForm()
    
#     if request.method == "POST":
#         form=UploadRestaurantDrinksProductsForm(request.POST or None, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request,f"File Uploaded Successfully")
#             return redirect('UploadRestaurantProductsPage')

#         messages.success(request,f"Failed to add upload file")
#         return redirect('UploadRestaurantDrinksProductsPage')


#     context = {
#         "form":form,
        

#     }
    
#     return render(request, 'RestaurantAddPage/UploadRestaurantDrinksProductsPage.html', context)





# @login_required(login_url='SigninPage')
# def UploadRestaurantRoomsProductsPage(request):
    
#     form = UploadRestaurantRoomsProductsForm()
    
#     if request.method == "POST":
#         form=UploadRestaurantRoomsProductsForm(request.POST or None, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request,f"File Uploaded Successfully")
#             return redirect('UploadRestaurantProductsPage')

#         messages.success(request,f"Failed to add upload file")
#         return redirect('UploadRestaurantRoomsProductsPage')


#     context = {
#         "form":form,
        

#     }
    
#     return render(request, 'RestaurantAddPage/UploadRestaurantRoomsProductsPage.html', context)




























#-------------------------Restaurant ORDERS--------------------------


@login_required(login_url='SigninPage')
def RestaurantOrdersPage(request):
    

    return render(request, 'RestaurantTemplatesApp/RestaurantOrdersPage.html')






#----------Restaurant FOOD ORDER PAGE---------------------------

@login_required(login_url='SigninPage')
def RestaurantOrderPage(request):
    queryset = RestaurantOrder.objects.all().order_by('-id')
    # Calculate the main total price for all orders
    main_total_price = queryset.aggregate(Sum('total_price'))['total_price__sum']
    print(main_total_price);
    get_sum = 0
    get_sum_filter_date = 0
    start_date = 0
    end_date = 0
    username = 0

    

    

    form = RestaurantOrderSearchForm(request.POST or None)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
        "main_total_price":main_total_price,
        "get_sum":get_sum,
        "get_sum_filter_date":get_sum_filter_date,
        "start_date":start_date,
        "end_date":end_date,
        "username":username,
    }





    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
        #category__icontains=form['category'].value(),
        user = form['user'].value()
        startDate = form['start_date'].value()
        endDate = form['end_date'].value()

        

        if (user != '' and startDate == '' and endDate == ''):

            selected_user = MyUser.objects.get(id=user)
            username = selected_user.username
            #print(f"USERNAME : {username}")


            
            queryset = RestaurantOrder.objects.all().order_by('-id')
            queryset = queryset.filter(user_id=user)



            



            get_sum = queryset.filter(
                user_id=user
            ).aggregate(sum=Sum('total_price'))

            

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)


        if (user != '' and startDate != '' and endDate != ''):

            selected_user = MyUser.objects.get(id=user)
            username = selected_user.username
            #print(f"USERNAME : {username}")

            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Adjust the date range by adding one day to the end date
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
            
            queryset = RestaurantOrder.objects.all().order_by('-id')
            queryset = queryset.filter(
                user_id=user,
                created__gte=start_date, 
                created__lte=end_date

                )



            get_sum = queryset.filter(
                user_id=user,
                created__gte=start_date, created__lte=end_date
            ).aggregate(sum=Sum('total_price'))

            

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)


        if (user == '' and startDate != '' and endDate != ''):
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Adjust the date range by adding one day to the end date
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)

            queryset = RestaurantOrder.objects.filter(
                # created__range=[

                #     form['start_date'].value(),
                #     form['end_date'].value()

                # ]
                created__gte=start_date, created__lte=end_date


                                            #product_name__icontains=form['product_name'].value(),
                                            #product_second_name__icontains=form['product_second_name'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            # start_date = request.POST.get('start_date')
            # end_date = request.POST.get('end_date')

            get_sum_filter_date = queryset.filter(
                created__gte=start_date, created__lte=end_date
                ).aggregate(sum=Sum('total_price'))

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)


        #hii ni kwa ajili ya kudownload ile page nzima ya stock endapo mtu akiweka tiki kwenye field export to csv
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['content-Disposition'] = 'attachment; filename="Food Orders.csv"'
            writer = csv.writer(response)
            writer.writerow(['Order ID', 'Ordered By', 'Total Price','Order Status', 'Ordered Date'])
            instance = queryset
            for x in queryset:
                writer.writerow([x.id,x.user.username,x.total_price,x.order_status,x.created])
            return response
            #ZINAISHIA HAPA ZA KUDOWNLOAD

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
        "main_total_price":main_total_price,
        "get_sum":get_sum,
        "get_sum_filter_date":get_sum_filter_date,
        "start_date":start_date,
        "end_date":end_date,
        "username":username,
    }


    return render(request, 'RestaurantTemplatesApp/RestaurantOrderPage.html', context)








@login_required(login_url='SigninPage')
def DeleteRestaurantOrder(request,id):
    x = RestaurantOrder.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Order was deleted Successfully")
    return redirect('RestaurantOrderPage')












#-------------------VIEW Restaurant FOOD ORDER ITEMS-----------------------

@login_required(login_url='SigninPage')
def ViewRestaurantOrderItemsPage(request, id):
    OrderId = RestaurantOrder.objects.get(id=id)


    queryset = RestaurantOrderItems.objects.filter(
                order__id__icontains = OrderId.id
                )

    get_sum = RestaurantOrderItems.objects.filter(
        order__id__icontains = OrderId.id
        ).aggregate(sum=Sum('price'))

    # queryset = RestaurantOrderItems.objects.all(
                
    #             )
    context = {
        "queryset": queryset,
        "OrderId": OrderId,
        "get_sum":get_sum,
        
    }
    

    return render(request, 'RestaurantTemplatesApp/ViewRestaurantOrderItemsPage.html',context)












#-----------------Restaurant DRINKS ORDERS------------------

@login_required(login_url='SigninPage')
def RestaurantDrinksOrderPage(request):
    queryset = RestaurantDrinksOrder.objects.all().order_by('-id')
    # Calculate the main total price for all orders
    main_total_price = queryset.aggregate(Sum('total_price'))['total_price__sum']
    print(main_total_price);
    get_sum = 0
    get_sum_filter_date = 0
    start_date = 0
    end_date = 0
    username = 0

    

    

    form = RestaurantDrinksOrderSearchForm(request.POST or None)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
        "main_total_price":main_total_price,
        "get_sum":get_sum,
        "get_sum_filter_date":get_sum_filter_date,
        "start_date":start_date,
        "end_date":end_date,
        "username":username,
    }





    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
        #category__icontains=form['category'].value(),
        user = form['user'].value()
        startDate = form['start_date'].value()
        endDate = form['end_date'].value()

        

        if (user != '' and startDate == '' and endDate == ''):

            selected_user = MyUser.objects.get(id=user)
            username = selected_user.username
            #print(f"USERNAME : {username}")


            
            queryset = RestaurantDrinksOrder.objects.all().order_by('-id')
            queryset = queryset.filter(user_id=user)



            



            get_sum = queryset.filter(
                user_id=user
            ).aggregate(sum=Sum('total_price'))

            

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)


        if (user != '' and startDate != '' and endDate != ''):

            selected_user = MyUser.objects.get(id=user)
            username = selected_user.username
            #print(f"USERNAME : {username}")

            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Adjust the date range by adding one day to the end date
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
            
            queryset = RestaurantDrinksOrder.objects.all().order_by('-id')
            queryset = queryset.filter(
                user_id=user,
                created__gte=start_date, 
                created__lte=end_date

                )



            get_sum = queryset.filter(
                user_id=user,
                created__gte=start_date, created__lte=end_date
            ).aggregate(sum=Sum('total_price'))

            

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)


        if (user == '' and startDate != '' and endDate != ''):
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Adjust the date range by adding one day to the end date
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)

            queryset = RestaurantDrinksOrder.objects.filter(
                # created__range=[

                #     form['start_date'].value(),
                #     form['end_date'].value()

                # ]
                created__gte=start_date, created__lte=end_date


                                            #product_name__icontains=form['product_name'].value(),
                                            #product_second_name__icontains=form['product_second_name'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            # start_date = request.POST.get('start_date')
            # end_date = request.POST.get('end_date')

            get_sum_filter_date = queryset.filter(
                created__gte=start_date, created__lte=end_date
                ).aggregate(sum=Sum('total_price'))

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)

        #hii ni kwa ajili ya kudownload ile page nzima ya stock endapo mtu akiweka tiki kwenye field export to csv
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['content-Disposition'] = 'attachment; filename="Drinks Orders.csv"'
            writer = csv.writer(response)
            writer.writerow(['Order ID', 'Ordered By', 'Total Price','Order Status', 'Ordered Date'])
            instance = queryset
            for x in queryset:
                writer.writerow([x.id,x.user.username,x.total_price,x.order_status,x.created])
            return response
            #ZINAISHIA HAPA ZA KUDOWNLOAD

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
        "main_total_price":main_total_price,
        "get_sum":get_sum,
        "get_sum_filter_date":get_sum_filter_date,
        "start_date":start_date,
        "end_date":end_date,
        "username":username,
    }


    return render(request, 'RestaurantTemplatesApp/RestaurantDrinksOrderPage.html', context)








@login_required(login_url='SigninPage')
def DeleteRestaurantDrinksOrder(request,id):
    x = RestaurantDrinksOrder.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Order was deleted Successfully")
    return redirect('RestaurantDrinksOrderPage')












#-------------------VIEW Restaurant Drinks ORDER ITEMS-----------------------

@login_required(login_url='SigninPage')
def ViewRestaurantDrinksOrderItemsPage(request, id):
    OrderId = RestaurantDrinksOrder.objects.get(id=id)


    queryset = RestaurantDrinksOrderItems.objects.filter(
                order__id__icontains = OrderId.id
                )

    get_sum = RestaurantDrinksOrderItems.objects.filter(
        order__id__icontains = OrderId.id
        ).aggregate(sum=Sum('price'))

    # queryset = RestaurantDrinksOrderItems.objects.all(
                
    #             )
    context = {
        "queryset": queryset,
        "OrderId": OrderId,
        "get_sum":get_sum,
        
    }
    

    return render(request, 'RestaurantTemplatesApp/ViewRestaurantDrinksOrderItemsPage.html',context)














#----------------Restaurant ROOMS ORDERS----------------------------

@login_required(login_url='SigninPage')
def RestaurantRoomsOrderPage(request):
    queryset = RestaurantRoomsOrder.objects.all().order_by('-id')
    # Calculate the main total price for all orders
    main_total_price = queryset.aggregate(Sum('total_price'))['total_price__sum']
    print(main_total_price);
    get_sum = 0
    get_sum_filter_date = 0
    start_date = 0
    end_date = 0
    username = 0

    

    

    form = RestaurantRoomsOrderSearchForm(request.POST or None)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
        "main_total_price":main_total_price,
        "get_sum":get_sum,
        "get_sum_filter_date":get_sum_filter_date,
        "start_date":start_date,
        "end_date":end_date,
        "username":username,
    }





    if request.method == "POST":
        #kwa ajili ya kufilter items and category ktk form
            
        #category__icontains=form['category'].value(),
        user = form['user'].value()
        startDate = form['start_date'].value()
        endDate = form['end_date'].value()

        

        if (user != '' and startDate == '' and endDate == ''):

            selected_user = MyUser.objects.get(id=user)
            username = selected_user.username
            #print(f"USERNAME : {username}")


            
            queryset = RestaurantRoomsOrder.objects.all().order_by('-id')
            queryset = queryset.filter(user_id=user)



            



            get_sum = queryset.filter(
                user_id=user
            ).aggregate(sum=Sum('total_price'))

            

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)


        if (user != '' and startDate != '' and endDate != ''):

            selected_user = MyUser.objects.get(id=user)
            username = selected_user.username
            #print(f"USERNAME : {username}")

            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Adjust the date range by adding one day to the end date
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)
            
            queryset = RestaurantRoomsOrder.objects.all().order_by('-id')
            queryset = queryset.filter(
                user_id=user,
                created__gte=start_date, 
                created__lte=end_date

                )



            get_sum = queryset.filter(
                user_id=user,
                created__gte=start_date, created__lte=end_date
            ).aggregate(sum=Sum('total_price'))

            

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)


        if (user == '' and startDate != '' and endDate != ''):
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')

            # Adjust the date range by adding one day to the end date
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d') + datetime.timedelta(days=1)

            queryset = RestaurantRoomsOrder.objects.filter(
                # created__range=[

                #     form['start_date'].value(),
                #     form['end_date'].value()

                # ]
                created__gte=start_date, created__lte=end_date


                                            #product_name__icontains=form['product_name'].value(),
                                            #product_second_name__icontains=form['product_second_name'].value()
                                            #last_updated__gte=form['start_date'].value(),
                                            # last_updated__lte=form['end_date'].value()
                                            #last_updated__range=[
                                                #form['start_date'].value(),
                                                #form['end_date'].value()
                                            #]
                )
            # start_date = request.POST.get('start_date')
            # end_date = request.POST.get('end_date')

            get_sum_filter_date = queryset.filter(
                created__gte=start_date, created__lte=end_date
                ).aggregate(sum=Sum('total_price'))

            #To SET  PAGINATION IN STOCK LIST PAGE
            paginator = Paginator(queryset,5)
            page = request.GET.get('page')
            try:
                queryset=paginator.page(page)
            except PageNotAnInteger:
                queryset=paginator.page(1)
            except EmptyPage:
                queryset=paginator.page(paginator.num_pages)


        #hii ni kwa ajili ya kudownload ile page nzima ya stock endapo mtu akiweka tiki kwenye field export to csv
        if form['export_to_CSV'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['content-Disposition'] = 'attachment; filename="Rooms Orders.csv"'
            writer = csv.writer(response)
            writer.writerow(['Order ID', 'Ordered By', 'Total Price','Order Status', 'Ordered Date'])
            instance = queryset
            for x in queryset:
                writer.writerow([x.id,x.user.username,x.total_price,x.order_status,x.created])
            return response
            #ZINAISHIA HAPA ZA KUDOWNLOAD

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
        "main_total_price":main_total_price,
        "get_sum":get_sum,
        "get_sum_filter_date":get_sum_filter_date,
        "start_date":start_date,
        "end_date":end_date,
        "username":username,
    }


    return render(request, 'RestaurantTemplatesApp/RestaurantRoomsOrderPage.html', context)








@login_required(login_url='SigninPage')
def DeleteRestaurantRoomsOrder(request,id):
    x = RestaurantRoomsOrder.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Order was deleted Successfully")
    return redirect('RestaurantRoomsOrderPage')












#-------------------VIEW Restaurant Rooms ORDER ITEMS-----------------------

@login_required(login_url='SigninPage')
def ViewRestaurantRoomsOrderItemsPage(request, id):
    OrderId = RestaurantRoomsOrder.objects.get(id=id)


    queryset = RestaurantRoomsOrderItems.objects.filter(
                order__id__icontains = OrderId.id
                )

    get_sum = RestaurantRoomsOrderItems.objects.filter(
        order__id__icontains = OrderId.id
        ).aggregate(sum=Sum('price'))

    # queryset = RestaurantRoomsOrderItems.objects.all(
                
    #             )
    context = {
        "queryset": queryset,
        "OrderId": OrderId,
        "get_sum":get_sum,
        
    }
    

    return render(request, 'RestaurantTemplatesApp/ViewRestaurantRoomsOrderItemsPage.html',context)



























#-----------------------Restaurant STAFF MAINTENANCE-----------------


#-------------------Restaurant STAFFS--------------------------------


@login_required(login_url='SigninPage')
def RestaurantMyUserPage(request):
    queryset = MyUser.objects.filter(is_restaurant_user=True).order_by('id')
    form = RestaurantMyUserSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            username = form.cleaned_data.get('username', '')
            email = form.cleaned_data.get('email', '')

            # Use Q objects to construct the query
            query = Q()
            if username:
                query |= Q(username__icontains=username)
            if email:
                query |= Q(email__icontains=email)

            queryset = MyUser.objects.filter(query)

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }

    return render(request, 'RestaurantTemplatesApp/RestaurantMyUserPage.html', context)


@login_required(login_url='SigninPage')
def Restaurant_search_username_RestaurantMyUser_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(username__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = MyUser.objects.filter(search)
    mylist= []
    mylist += [x.username for x in queryset]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Restaurant_search_email_RestaurantMyUser_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(email__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = MyUser.objects.filter(search)
    mylist= []
    mylist += [x.email for x in queryset]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantMyUser(request,id):
    x = MyUser.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Staff was deleted Successfully")
    return redirect('RestaurantMyUserPage')




















#-----------------Restaurant  SUPPLIER---------------------------


@login_required(login_url='SigninPage')
def RestaurantSuppliersPage(request):
    queryset = RestaurantSuppliers.objects.all().order_by('-id')

    form = RestaurantSuppliersSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            SupplierFullName = form.cleaned_data.get('SupplierFullName', '')
            Keyword = form.cleaned_data.get('Keyword', '')
            #Status = form.cleaned_data.get('Status', '')
            

            

            # Use Q objects to construct the query
            query = Q()
            if SupplierFullName:
                query |= Q(SupplierFullName__icontains=SupplierFullName)

            if Keyword:
                query |= Q(Keyword__icontains=Keyword)

            # if Status:
            #     query |= Q(Status__icontains=Status)
                        

            queryset = RestaurantSuppliers.objects.filter(query)
    

    #To SET  PAGINATION IN STOCK LIST PAGE
    paginator = Paginator(queryset,5)
    page = request.GET.get('page')
    try:
        queryset=paginator.page(page)
    except PageNotAnInteger:
        queryset=paginator.page(1)
    except EmptyPage:
        queryset=paginator.page(paginator.num_pages)

    context = {
        "queryset": queryset,
        "form": form,
        "page":page,
    }


    # if request.method == "POST":
    #     #kwa ajili ya kufilter items and category ktk form
            
    #         #category__icontains=form['category'].value(),
    #         Status = form['Status'].value()

            

                                            
    #         queryset = RestaurantSuppliers.objects.filter(
    #                                         SupplierFullName__icontains=form['SupplierFullName'].value(),
    #                                         Keyword__icontains=form['Keyword'].value()
    #                                         #last_updated__gte=form['start_date'].value(),
    #                                         # last_updated__lte=form['end_date'].value()
    #                                         #last_updated__range=[
    #                                             #form['start_date'].value(),
    #                                             #form['end_date'].value()
    #                                         #]
    #             )
    #         if (Status != ''):
    #             queryset = RestaurantSuppliers.objects.all().order_by('-id')
    #             queryset = queryset.filter(Status=Status)

    #             #To SET  PAGINATION IN STOCK LIST PAGE
    #             paginator = Paginator(queryset,5)
    #             page = request.GET.get('page')
    #             try:
    #                 queryset=paginator.page(page)
    #             except PageNotAnInteger:
    #                 queryset=paginator.page(1)
    #             except EmptyPage:
    #                 queryset=paginator.page(paginator.num_pages)

    # context = {
    #     "queryset": queryset,
    #     "form": form,
    #     "page":page,
    # }

    return render(request, 'RestaurantTemplatesApp/RestaurantSuppliersPage.html', context)





@login_required(login_url='SigninPage')
def Restaurant_search_SupplierFullName_RestaurantSuppliers_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(SupplierFullName__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = RestaurantSuppliers.objects.filter(search)
    mylist= []
    mylist += [x.SupplierFullName for x in queryset]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def Restaurant_search_Keyword_RestaurantSuppliers_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Keyword__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = RestaurantSuppliers.objects.filter(search)
    mylist= []
    mylist += [x.Keyword for x in queryset]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRestaurantSuppliers(request,id):
    x = RestaurantSuppliers.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Supplier was deleted Successfully")
    return redirect('RestaurantSuppliersPage')



@login_required(login_url='SigninPage')
def AddRestaurantSuppliers(request):
    
    form = AddRestaurantSuppliersForm()
    
    if request.method == "POST":
        form=AddRestaurantSuppliersForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RestaurantSuppliersPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRestaurantSuppliers')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RestaurantAddPage/AddRestaurantSuppliers.html', context)



@login_required(login_url='SigninPage')
def UpdateRestaurantSuppliers(request,id):
    x = RestaurantSuppliers.objects.get(id=id)
    form = AddRestaurantSuppliersForm(instance=x)
    
    if request.method == "POST":
        form=AddRestaurantSuppliersForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RestaurantSuppliersPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RestaurantUpdatePage/UpdateRestaurantSuppliers.html', context)











#---------------UPLOAD PRODUCTS----------------------




#--------------UPLOAD FOOD PRODUCTS--------------------
def UploadRestaurantProductsPage(request):
    if request.method == "POST":
        item_resource = RestaurantProductsResource()
        dataset = Dataset()
        new_item_resource = request.FILES['myfile']

        if not new_item_resource.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request, 'RestaurantAddPage/UploadRestaurantProductsPage.html')


        imported_data = dataset.load(new_item_resource.read(), format='xlsx')

        for data in imported_data:
            value = RestaurantProducts(
                data[0], #ID
                data[1], #StoreCode
                data[2], #StoreBinCode
                data[3], #Unit
                data[4], #product_name
                data[5], #product_second_name
                data[6], #productCategory
                data[7], #price
                data[8], #ProductQuantity
                data[9], #InitialProductQuantity
                data[10] #CategoryImage
                # data[11], #Created
                # data[12] #Updated
                )
            value.save()
        messages.success(request, 'Data Uploaded successfully')
    return render(request, 'RestaurantAddPage/UploadRestaurantProductsPage.html')



    #return HttpResponse("File Uploaded Successfully")









#--------------UPLOAD DRINKS PRODUCTS--------------------
def UploadRestaurantDrinksProductsPage(request):
    if request.method == "POST":
        item_resource = RestaurantDrinksProductsResource()
        dataset = Dataset()
        new_item_resource = request.FILES['myfile']

        if not new_item_resource.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request, 'RestaurantAddPage/UploadRestaurantDrinksProductsPage.html')


        imported_data = dataset.load(new_item_resource.read(), format='xlsx')

        for data in imported_data:
            value = RestaurantDrinksProducts(
                data[0], #ID
                data[1], #StoreCode
                data[2], #StoreBinCode
                data[3], #Unit
                data[4], #product_name
                data[5], #product_second_name
                data[6], #productCategory
                data[7], #price
                data[8], #ProductQuantity
                data[9], #InitialProductQuantity
                data[10] #CategoryImage
                # data[11], #Created
                # data[12] #Updated
                )
            value.save()
        messages.success(request, 'Data Uploaded successfully')
    return render(request, 'RestaurantAddPage/UploadRestaurantDrinksProductsPage.html')



    #return HttpResponse("File Uploaded Successfully")








