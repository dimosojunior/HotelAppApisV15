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
from RetailsApis.models import *

UserModel = get_user_model()


#tunadisplay users wote ambao wapo active lakini  hawajalipa yani
#bila kuweka paid status ili uweze kuwaadeactivate mmoja mmoja

@login_required(login_url='SigninPage')
def RetailsDeactivateUsersPage(request):

    queryset = MyUser.objects.filter(
        #is_active=True,
        is_superuser=False,
        is_retails_user=True,
        is_paid=True

        ).order_by('-id')

    get_unpaid_sum = MyUser.objects.filter(
        #is_active=True,
        is_superuser=False,
        is_retails_user=True,
        is_paid=True
        ).count()


    form = UnpaidRetailsMyUserSearchForm(request.POST or None)

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

    return render(request, 'RetailsTemplatesApp/RetailsDeactivateUsersPage.html', context)






@login_required(login_url='SigninPage')
def Retails_search_username_UnpaidRetailsMyUser_autocomplete(request):
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
def Retails_search_email_UnpaidRetailsMyUser_autocomplete(request):
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
def Retails_search_company_name_UnpaidRetailsMyUser_autocomplete(request):
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
def UpdateUnpaidRetailsMyUser(request,id):
    x = MyUser.objects.get(id=id)
    form = UpdateUnpaidRetailsMyUserForm(instance=x)
    
    if request.method == "POST":
        form=UpdateUnpaidRetailsMyUserForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()


            subject = "Your account has been deactivated"
            message = "Your account has been deactivated "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [x.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsDeactivateUsersPage')

        messages.success(request,f"Fail to update data")
        return redirect('UpdateUnpaidRetailsMyUser', id=id)

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateUnpaidRetailsMyUser.html', context)












#tunawadisplay users wote ambao accunt zao zipo inactive ili twweze
#kuwaactivate mmoja mmoja, ila paid ni False ili tuweze kuona wote ambao
#ccount zao zilikuwa deactivated then tuziactivate
@login_required(login_url='SigninPage')
def RetailsactivateUsersPage(request):

    queryset = MyUser.objects.filter(
        #is_active=False,
        is_superuser=False,
        is_retails_user=True,
        is_paid=False

        ).order_by('-id')

    get_paid_sum = MyUser.objects.filter(
        #is_active=False,
        is_superuser=False,
        is_retails_user=True,
        is_paid=False
        ).count()


    form = paidRetailsMyUserSearchForm(request.POST or None)

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

    return render(request, 'RetailsTemplatesApp/RetailsactivateUsersPage.html',context)






@login_required(login_url='SigninPage')
def Retails_search_username_paidRetailsMyUser_autocomplete(request):
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
def Retails_search_email_paidRetailsMyUser_autocomplete(request):
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
def Retails_search_company_name_paidRetailsMyUser_autocomplete(request):
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
def UpdatepaidRetailsMyUser(request,id):
    x = MyUser.objects.get(id=id)
    form = UpdatepaidRetailsMyUserForm(instance=x)
    
    if request.method == "POST":
        form=UpdatepaidRetailsMyUserForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()


            subject = "Your account has been activated"
            message = "Your account has been activated "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [x.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)

            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsactivateUsersPage')

        messages.success(request,f"Fail to update data")
        return redirect('UpdatepaidRetailsMyUser', id=id)

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdatepaidRetailsMyUser.html', context)









@login_required(login_url='SigninPage')
def RetailsHomePage(request):

    return render(request, 'RetailsTemplatesApp/Retailshome.html')


#hapa tunafungiwa wote kwa pamoja ambao account zao zipo active 
#lakini hawajalipa
@login_required(login_url='SigninPage')
def Retailsdeactivate_inactive_users(request):
    # Get the current date
    current_date = timezone.now()
    # Calculate the date threshold (1 days ago)
    threshold_date = current_date - timezone.timedelta(days=1)

    # Get all users whose registration date is older than 1 days
    users_to_deactivate = MyUser.objects.filter(
        date_joined__lt=threshold_date, 
        #is_active=True,
        is_superuser=False,
        is_retails_user=True,
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
    return redirect("RetailsDeactivateUsersPage")


#hapa tunawaactivate wote kwa pamoja ambao account zao zipo inactive 
#lakini wamelipa
@login_required(login_url='SigninPage')
def Retailsactivate_inactive_users(request):
    # Get the current date
    current_date = timezone.now()
    # Calculate the date threshold (1 days ago)
    threshold_date = current_date - timezone.timedelta(days=1)

    # Get all users whose registration date is older than 1 days
    users_to_deactivate = MyUser.objects.filter(
        date_joined__lt=threshold_date, 
        #is_active=False ,
        is_superuser = False,
        is_retails_user=True,
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
    return redirect("RetailsactivateUsersPage")





def RetailsSignupPage(request):
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
            return redirect('RetailsSignupPage')
    else:
        form = MyUserForm()

    context = {
        "form": form
    }
    return render(request, 'Account/RetailsSignupPage.html', context)





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




class RetailsPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    #login_url = 'login'
    success_url = reverse_lazy('RetailsHomePage')




@login_required(login_url='SigninPage')
def RetailsUpdateUser(request, id):
    x = MyUser.objects.get(id=id)
    if request.method == "POST":
        form = UpdateMyUserForm(request.POST, instance=x)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'{x.username} is updated successfully')
            return redirect('RetailsUpdateUser',id=id)
    else:
        form = UpdateMyUserForm(instance=x)

    context = {
        "form": form
    }
    return render(request, 'Account/RetailsUpdateUser.html', context)










































#-------------------CUSTOMERS--------------------------------


@login_required(login_url='SigninPage')
def RetailsCustomersPage(request):
    customers = RetailsCustomers.objects.all().order_by('-id')
    form = RetailsCustomersSearchForm(request.POST or None)

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

            customers = RetailsCustomers.objects.filter(query)

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

    return render(request, 'RetailsTemplatesApp/RetailsCustomersPage.html', context)





@login_required(login_url='SigninPage')
def Retails_search_customer_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CustomerFullName__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    customers = RetailsCustomers.objects.filter(search)
    mylist= []
    mylist += [x.CustomerFullName for x in customers]
    return JsonResponse(mylist, safe=False)

def Retails_search_address_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CustomerAddress__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    customers = RetailsCustomers.objects.filter(search)
    mylist= []
    mylist += [x.CustomerAddress for x in customers]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def DeleteRetailsCustomerPage(request,id):
    x = RetailsCustomers.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"{x.CustomerFullName} was deleted Successfully")
    return redirect('RetailsCustomersPage')
    



@login_required(login_url='SigninPage')
def AddRetailsCustomerPage(request):
    
    form = AddRetailsCustomerForm()
    
    if request.method == "POST":
        form=AddRetailsCustomerForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsCustomersPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsCustomerPage')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsCustomerPage.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsCustomerPage(request,id):
    x = RetailsCustomers.objects.get(id=id)
    form = AddRetailsCustomerForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsCustomerForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"{x.CustomerFullName}   updated Successfully")
            return redirect('RetailsCustomersPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsCustomerPage.html', context)










#---------------BUSINESS UNIT--------------------

@login_required(login_url='SigninPage')
def RetailsBusinessUnitPage(request):
    queryset = RetailsBusinessUnit.objects.all().order_by('-id')
    form = RetailsBusinessUnitSearchForm(request.POST or None)

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

            queryset = RetailsBusinessUnit.objects.filter(query)

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

    return render(request, 'RetailsTemplatesApp/RetailsBusinessUnitPage.html', context)





@login_required(login_url='SigninPage')
def Retails_search_Code_Business_Unit_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsBusinessUnit.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Retails_search_Description_Business_Unit_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsBusinessUnit.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRetailsBusinessUnit(request,id):
    x = RetailsBusinessUnit.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Business Unit with code {x.Code} was deleted Successfully")
    return redirect('RetailsBusinessUnitPage')
    

    


@login_required(login_url='SigninPage')
def AddRetailsBusinessUnit(request):
    
    form = AddRetailsBusinessUnitForm()
    
    if request.method == "POST":
        form=AddRetailsBusinessUnitForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsBusinessUnitPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsBusinessUnit')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsBusinessUnit.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsBusinessUnit(request,id):
    x = RetailsBusinessUnit.objects.get(id=id)
    form = AddRetailsBusinessUnitForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsBusinessUnitForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsBusinessUnitPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsBusinessUnit.html', context)





















#---------------LOCATION CODE UNIT--------------------

@login_required(login_url='SigninPage')
def RetailsLocationCodePage(request):
    queryset = RetailsLocationCode.objects.all().order_by('-id')
    form = RetailsLocationCodeSearchForm(request.POST or None)

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

            queryset = RetailsLocationCode.objects.filter(query)

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

            

                                            
            queryset = RetailsLocationCode.objects.filter(
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
                queryset = RetailsLocationCode.objects.all()
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

    return render(request, 'RetailsTemplatesApp/RetailsLocationCodePage.html', context)





@login_required(login_url='SigninPage')
def Retails_search_Code_Location_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsLocationCode.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Retails_search_Description_Location_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsLocationCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRetailsLocationCode(request,id):
    x = RetailsLocationCode.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Business Unit with code {x.Code} was deleted Successfully")
    return redirect('RetailsLocationCodePage')
    

    


@login_required(login_url='SigninPage')
def AddRetailsLocationCode(request):
    
    form = AddRetailsLocationCodeForm()
    
    if request.method == "POST":
        form=AddRetailsLocationCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsLocationCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsLocationCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsLocationCode.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsLocationCode(request,id):
    x = RetailsLocationCode.objects.get(id=id)
    form = AddRetailsLocationCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsLocationCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsLocationCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsLocationCode.html', context)












#----------------------Retails PROCESS CONFIG-----------------------




@login_required(login_url='SigninPage')
def RetailsProcessConfigPage(request):
    queryset = RetailsProcessConfig.objects.all().order_by('-id')
    form = RetailsProcessConfigSearchForm(request.POST or None)

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

            queryset = RetailsProcessConfig.objects.filter(query)


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

    

    return render(request, 'RetailsTemplatesApp/RetailsProcessConfigPage.html', context)





@login_required(login_url='SigninPage')
def Retails_search_ProcesId_process_config_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(ProcesId__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsProcessConfig.objects.filter(search)
    mylist= []
    mylist += [x.ProcesId for x in filters]
    return JsonResponse(mylist, safe=False)

def Retails_search_Description_process_config_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsProcessConfig.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRetailsProcessConfig(request,id):
    x = RetailsProcessConfig.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data deleted Successfully")
    return redirect('RetailsProcessConfigPage')
    

    


@login_required(login_url='SigninPage')
def AddRetailsProcessConfig(request):
    
    form = AddRetailsProcessConfigForm()
    
    if request.method == "POST":
        form=AddRetailsProcessConfigForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsProcessConfigPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsProcessConfig')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsProcessConfig.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsProcessConfig(request,id):
    x = RetailsProcessConfig.objects.get(id=id)
    form = AddRetailsProcessConfigForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsProcessConfigForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsProcessConfigPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsProcessConfig.html', context)





















#---------------Retails STORE CODE--------------------

@login_required(login_url='SigninPage')
def RetailsStoreCodePage(request):
    queryset = RetailsStoreCode.objects.all().order_by('-id')
    form = RetailsStoreCodeSearchForm(request.POST or None)

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

            queryset = RetailsStoreCode.objects.filter(query)

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


            

                                            
            queryset = RetailsStoreCode.objects.filter(
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
                queryset = RetailsStoreCode.objects.all()
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
                queryset = RetailsStoreCode.objects.all()
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

    return render(request, 'RetailsTemplatesApp/RetailsStoreCodePage.html', context)

    





@login_required(login_url='SigninPage')
def Retails_search_Code_store_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsStoreCode.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

def Retails_search_Description_store_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsStoreCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRetailsStoreCode(request,id):
    x = RetailsStoreCode.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data {x.Code} was deleted Successfully")
    return redirect('RetailsStoreCodePage')
    

    


@login_required(login_url='SigninPage')
def AddRetailsStoreCode(request):
    
    form = AddRetailsStoreCodeForm()
    
    if request.method == "POST":
        form=AddRetailsStoreCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsStoreCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsStoreCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsStoreCode.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsStoreCode(request,id):
    x = RetailsStoreCode.objects.get(id=id)
    form = AddRetailsStoreCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsStoreCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsStoreCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsStoreCode.html', context)
















#----------------------Retails STORE BIN CODE-----------------------




@login_required(login_url='SigninPage')
def RetailsStoreBinCodePage(request):
    queryset = RetailsStoreBinCode.objects.all().order_by('-id')
    form = RetailsStoreBinCodeSearchForm(request.POST or None)

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

            queryset = RetailsStoreBinCode.objects.filter(query)


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

    

    return render(request, 'RetailsTemplatesApp/RetailsStoreBinCodePage.html', context)





@login_required(login_url='SigninPage')
def Retails_search_StoreBinCode_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(StoreBinCode__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.StoreBinCode for x in filters]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Retails_search_CardNo_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(CardNo__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.CardNo for x in filters]
    return JsonResponse(mylist, safe=False)


def Retails_search_Description_store_bin_code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsStoreBinCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRetailsStoreBinCode(request,id):
    x = RetailsStoreBinCode.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data deleted Successfully")
    return redirect('RetailsStoreBinCodePage')
    

    


@login_required(login_url='SigninPage')
def AddRetailsStoreBinCode(request):
    
    form = AddRetailsStoreBinCodeForm()
    
    if request.method == "POST":
        form=AddRetailsStoreBinCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsStoreBinCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsStoreBinCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsStoreBinCode.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsStoreBinCode(request,id):
    x = RetailsStoreBinCode.objects.get(id=id)
    form = AddRetailsStoreBinCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsStoreBinCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsStoreBinCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsStoreBinCode.html', context)















#-------------------------EVENT CODES---------------------------


@login_required(login_url='SigninPage')
def RetailsEventCodePage(request):
    queryset = RetailsEventCode.objects.all().order_by('-id')
    form = RetailsEventCodeSearchForm(request.POST or None)

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

            queryset = RetailsEventCode.objects.filter(query)

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

    return render(request, 'RetailsTemplatesApp/RetailsEventCodePage.html', context)





@login_required(login_url='SigninPage')
def Retails_search_Code_Event_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsEventCode.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Retails_search_Description_Event_Code_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Description__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsEventCode.objects.filter(search)
    mylist= []
    mylist += [x.Description for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRetailsEventCode(request,id):
    x = RetailsEventCode.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RetailsEventCodePage')
    

    


@login_required(login_url='SigninPage')
def AddRetailsEventCode(request):
    
    form = AddRetailsEventCodeForm()
    
    if request.method == "POST":
        form=AddRetailsEventCodeForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsEventCodePage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsEventCode')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsEventCode.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsEventCode(request,id):
    x = RetailsEventCode.objects.get(id=id)
    form = AddRetailsEventCodeForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsEventCodeForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsEventCodePage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsEventCode.html', context)
















#-----------------Retails EVENT ALERT---------------------

@login_required(login_url='SigninPage')
def RetailsEventAlertPage(request):
    queryset = RetailsEventAlert.objects.all().order_by('-id')
    form = RetailsEventAlertSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            AlertID = form.cleaned_data.get('AlertID', '')
            

            # Use Q objects to construct the query
            query = Q()
            if AlertID:
                query |= Q(AlertID__icontains=AlertID)
            

            queryset = RetailsEventAlert.objects.filter(query)

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

    return render(request, 'RetailsTemplatesApp/RetailsEventAlertPage.html', context)





@login_required(login_url='SigninPage')
def Retails_search_Code_AlertID_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(AlertID__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsEventAlert.objects.filter(search)
    mylist= []
    mylist += [x.AlertID for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRetailsEventAlert(request,id):
    x = RetailsEventAlert.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RetailsEventAlertPage')
    

    


@login_required(login_url='SigninPage')
def AddRetailsEventAlert(request):
    
    form = AddRetailsEventAlertForm()
    
    if request.method == "POST":


        form=AddRetailsEventAlertForm(request.POST or None, files=request.FILES)
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
            return redirect('RetailsEventAlertPage')

        messages.success(request,f"Failed to add new alert")
        return redirect('AddRetailsEventAlert')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsEventAlert.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsEventAlert(request,id):
    x = RetailsEventAlert.objects.get(id=id)
    form = AddRetailsEventAlertForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsEventAlertForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Alert updated Successfully")
            return redirect('RetailsEventAlertPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsEventAlert.html', context)












#---------------UOM SHORT CODES--------------------

@login_required(login_url='SigninPage')
def RetailsUOMPage(request):
    queryset = RetailsUOM.objects.all().order_by('-id')
    form = RetailsUOMSearchForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():  # Check if the form is valid
            UOMShortCode = form.cleaned_data.get('UOMShortCode', '')
            

            # Use Q objects to construct the query
            query = Q()
            if UOMShortCode:
                query |= Q(UOMShortCode__icontains=UOMShortCode)
            

            queryset = RetailsUOM.objects.filter(query)

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

    return render(request, 'RetailsTemplatesApp/RetailsUOMPage.html', context)





@login_required(login_url='SigninPage')
def Retails_search_UOMShortCode_RetailsUOM_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(UOMShortCode__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsUOM.objects.filter(search)
    mylist= []
    mylist += [x.UOMShortCode for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRetailsUOM(request,id):
    x = RetailsUOM.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RetailsUOMPage')
    

    


@login_required(login_url='SigninPage')
def AddRetailsUOM(request):
    
    form = AddRetailsUOMForm()
    
    if request.method == "POST":
        form=AddRetailsUOMForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsUOMPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsUOM')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsUOM.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsUOM(request,id):
    x = RetailsUOM.objects.get(id=id)
    form = AddRetailsUOMForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsUOMForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsUOMPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsUOM.html', context)















#---------------BOM SHORT CODES--------------------

@login_required(login_url='SigninPage')
def RetailsBOMPage(request):
    queryset = RetailsBOM.objects.all().order_by('-id')
    form = RetailsBOMSearchForm(request.POST or None)

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
            

            queryset = RetailsBOM.objects.filter(query)

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

    return render(request, 'RetailsTemplatesApp/RetailsBOMPage.html', context)





@login_required(login_url='SigninPage')
def Retails_search_Code_RetailsBOM_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Code__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsBOM.objects.filter(search)
    mylist= []
    mylist += [x.Code for x in filters]
    return JsonResponse(mylist, safe=False)

@login_required(login_url='SigninPage')
def Retails_search_Name_RetailsBOM_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsBOM.objects.filter(search)
    mylist= []
    mylist += [x.Name for x in filters]
    return JsonResponse(mylist, safe=False)




@login_required(login_url='SigninPage')
def DeleteRetailsBOM(request,id):
    x = RetailsBOM.objects.get(id=id)

    
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RetailsBOMPage')
    

    


@login_required(login_url='SigninPage')
def AddRetailsBOM(request):
    
    form = AddRetailsBOMForm()
    
    if request.method == "POST":
        form=AddRetailsBOMForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsBOMPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsBOM')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsBOM.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsBOM(request,id):
    x = RetailsBOM.objects.get(id=id)
    form = AddRetailsBOMForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsBOMForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsBOMPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsBOM.html', context)







#----------------BOM DETAIL PAGE--------------------
@login_required(login_url='SigninPage')
def RetailsBOMDetailPage(request):
    queryset = RetailsBOM.objects.all().order_by('-id')
    form = RetailsBOMSearchForm(request.POST or None)

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
            

            queryset = RetailsBOM.objects.filter(query)

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

    return render(request, 'RetailsTemplatesApp/RetailsBOMDetailPage.html', context)










#------------BOM UPLOAD FILE----------------------------

@login_required(login_url='SigninPage')
def AddRetailsBOMFiles(request):
    
    form = AddRetailsBOMFilesForm()
    
    if request.method == "POST":
        form=AddRetailsBOMFilesForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"File Uploaded Successfully")
            return redirect('AddRetailsBOMFiles')

        messages.success(request,f"Failed to add upload file")
        return redirect('AddRetailsBOMFiles')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsBOMFiles.html', context)




























#----------------------SALES& DISTRIBUTION-----------------



#------------PRODUCTS CATEGORIES----------------------------

@login_required(login_url='SigninPage')
def RetailsProductsCategoriesPage(request):
    food = RetailsCategories.objects.all().order_by('-id')
    drinks = RetailsDrinksCategories.objects.all().order_by('-id')
    

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

    return render(request, 'RetailsTemplatesApp/RetailsProductsCategoriesPage.html', context)











#--------------------FOOD PRODUCTS CATEGORIES-------------------


#---------------------VIEW FOOD PRODUCT CATEGORY------------------
@login_required(login_url='SigninPage')
def ViewRetailsCategoriesPage(request,id):
    queryset = RetailsCategories.objects.get(id=id)

    form = AddRetailsCategoriesForm()
    
    if request.method == "POST":
        form=AddRetailsCategoriesForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data added successfully")
            return redirect('RetailsProductsCategoriesPage')

        messages.success(request,f"Failed to add new data")
        return redirect('ViewRetailsCategoriesPage',id=id)

    context = {
        "queryset": queryset,
        "form":form,
        
    }

    return render(request, 'ViewPages/ViewRetailsCategoriesPage.html', context)



#------------UPDATE FOOD PRODUCTS CATEGORIES--------------
@login_required(login_url='SigninPage')
def UpdateRetailsCategories(request,id):
    x = RetailsCategories.objects.get(id=id)
    form = AddRetailsCategoriesForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsCategoriesForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('ViewRetailsCategoriesPage',id=id)

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsCategories.html', context)



@login_required(login_url='SigninPage')
def DeleteRetailsCategories(request,id):
    x = RetailsCategories.objects.get(id=id)

    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RetailsProductsCategoriesPage')
    















#--------------------Drinks PRODUCTS CATEGORIES-------------------


#---------------------VIEW Drinks PRODUCT CATEGORY------------------
@login_required(login_url='SigninPage')
def ViewRetailsDrinksCategoriesPage(request,id):
    queryset = RetailsDrinksCategories.objects.get(id=id)

    form = AddRetailsDrinksCategoriesForm()
    
    if request.method == "POST":
        form=AddRetailsDrinksCategoriesForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data added successfully")
            return redirect('RetailsProductsCategoriesPage')

        messages.success(request,f"Failed to add new data")
        return redirect('ViewRetailsDrinksCategoriesPage',id=id)

    context = {
        "queryset": queryset,
        "form":form,
        
    }

    return render(request, 'ViewPages/ViewRetailsDrinksCategoriesPage.html', context)



#------------UPDATE Drinks PRODUCTS CATEGORIES--------------
@login_required(login_url='SigninPage')
def UpdateRetailsDrinksCategories(request,id):
    x = RetailsDrinksCategories.objects.get(id=id)
    form = AddRetailsDrinksCategoriesForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsDrinksCategoriesForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('ViewRetailsDrinksCategoriesPage',id=id)

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsDrinksCategories.html', context)



@login_required(login_url='SigninPage')
def DeleteRetailsDrinksCategories(request,id):
    x = RetailsDrinksCategories.objects.get(id=id)

    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RetailsProductsCategoriesPage')
































#-------------MAINTENANCE OF PRODUCTS ITSELF------------------



@login_required(login_url='SigninPage')
def RetailsProductsPage(request):
    

    return render(request, 'RetailsTemplatesApp/RetailsProductsPage.html')




#-------------------FOOD PRODUCTS-------------------------

@login_required(login_url='SigninPage')
def RetailsProductsPage(request):
    queryset = RetailsProducts.objects.all().order_by('-id')

    form = RetailsProductsSearchForm(request.POST or None)

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
            

            queryset = RetailsProducts.objects.filter(query)
    

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

            

                                            
            queryset = RetailsProducts.objects.filter(
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
                queryset = RetailsProducts.objects.all().order_by('-id')
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

    return render(request, 'RetailsTemplatesApp/RetailsProductsPage.html', context)

@login_required(login_url='SigninPage')
def search_product_name_RetailsProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_name for x in filters]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def search_product_second_name_RetailsProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_second_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_second_name for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRetailsProducts(request,id):
    x = RetailsProducts.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RetailsProductsPage')
    



@login_required(login_url='SigninPage')
def AddRetailsProducts(request):
    
    form = AddRetailsProductsForm()
    
    if request.method == "POST":
        form=AddRetailsProductsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsProductsPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsProducts')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsProducts.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsProducts(request,id):
    x = RetailsProducts.objects.get(id=id)
    form = AddRetailsProductsForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsProductsForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsProductsPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsProducts.html', context)


























#-------------------DRINKS PRODUCTS-------------------------

@login_required(login_url='SigninPage')
def RetailsDrinksProductsPage(request):
    queryset = RetailsDrinksProducts.objects.all().order_by('-id')

    form = RetailsDrinksProductsSearchForm(request.POST or None)

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
            

            queryset = RetailsDrinksProducts.objects.filter(query)
    

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

            

                                            
            queryset = RetailsDrinksProducts.objects.filter(
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
                queryset = RetailsDrinksProducts.objects.all().order_by('-id')
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

    return render(request, 'RetailsTemplatesApp/RetailsDrinksProductsPage.html', context)

@login_required(login_url='SigninPage')
def search_product_name_RetailsDrinksProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsDrinksProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_name for x in filters]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def search_product_second_name_RetailsDrinksProducts_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(product_second_name__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    filters = RetailsDrinksProducts.objects.filter(search)
    mylist= []
    mylist += [x.product_second_name for x in filters]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRetailsDrinksProducts(request,id):
    x = RetailsDrinksProducts.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Data was deleted Successfully")
    return redirect('RetailsDrinksProductsPage')
    



@login_required(login_url='SigninPage')
def AddRetailsDrinksProducts(request):
    
    form = AddRetailsDrinksProductsForm()
    
    if request.method == "POST":
        form=AddRetailsDrinksProductsForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsDrinksProductsPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsDrinksProducts')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsDrinksProducts.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsDrinksProducts(request,id):
    x = RetailsDrinksProducts.objects.get(id=id)
    form = AddRetailsDrinksProductsForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsDrinksProductsForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsDrinksProductsPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsDrinksProducts.html', context)













































@login_required(login_url='SigninPage')
def UploadRetailsProductsPage(request):
    

    return render(request, 'RetailsTemplatesApp/UploadRetailsProductsPage.html')





# @login_required(login_url='SigninPage')
# def UploadRetailsProductsPage(request):
    
#     form = UploadRetailsProductsForm()
    
#     if request.method == "POST":
#         form=UploadRetailsProductsForm(request.POST or None, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request,f"File Uploaded Successfully")
#             return redirect('UploadRetailsProductsPage')

#         messages.success(request,f"Failed to add upload file")
#         return redirect('UploadRetailsProductsPage')


#     context = {
#         "form":form,
        

#     }
    
#     return render(request, 'RetailsAddPage/UploadRetailsProductsPage.html', context)



# @login_required(login_url='SigninPage')
# def UploadRetailsDrinksProductsPage(request):
    
#     form = UploadRetailsDrinksProductsForm()
    
#     if request.method == "POST":
#         form=UploadRetailsDrinksProductsForm(request.POST or None, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request,f"File Uploaded Successfully")
#             return redirect('UploadRetailsProductsPage')

#         messages.success(request,f"Failed to add upload file")
#         return redirect('UploadRetailsDrinksProductsPage')


#     context = {
#         "form":form,
        

#     }
    
#     return render(request, 'RetailsAddPage/UploadRetailsDrinksProductsPage.html', context)





# @login_required(login_url='SigninPage')
# def UploadRetailsRoomsProductsPage(request):
    
#     form = UploadRetailsRoomsProductsForm()
    
#     if request.method == "POST":
#         form=UploadRetailsRoomsProductsForm(request.POST or None, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request,f"File Uploaded Successfully")
#             return redirect('UploadRetailsProductsPage')

#         messages.success(request,f"Failed to add upload file")
#         return redirect('UploadRetailsRoomsProductsPage')


#     context = {
#         "form":form,
        

#     }
    
#     return render(request, 'RetailsAddPage/UploadRetailsRoomsProductsPage.html', context)




























#-------------------------Retails ORDERS--------------------------


@login_required(login_url='SigninPage')
def RetailsOrdersPage(request):
    

    return render(request, 'RetailsTemplatesApp/RetailsOrdersPage.html')






#----------Retails FOOD ORDER PAGE---------------------------

@login_required(login_url='SigninPage')
def RetailsOrderPage(request):
    queryset = RetailsOrder.objects.all().order_by('-id')
    # Calculate the main total price for all orders
    main_total_price = queryset.aggregate(Sum('total_price'))['total_price__sum']
    print(main_total_price);
    get_sum = 0
    get_sum_filter_date = 0
    start_date = 0
    end_date = 0
    username = 0

    

    

    form = RetailsOrderSearchForm(request.POST or None)
    

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


            
            queryset = RetailsOrder.objects.all().order_by('-id')
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
            
            queryset = RetailsOrder.objects.all().order_by('-id')
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

            queryset = RetailsOrder.objects.filter(
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


    return render(request, 'RetailsTemplatesApp/RetailsOrderPage.html', context)








@login_required(login_url='SigninPage')
def DeleteRetailsOrder(request,id):
    x = RetailsOrder.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Order was deleted Successfully")
    return redirect('RetailsOrderPage')












#-------------------VIEW Retails FOOD ORDER ITEMS-----------------------

@login_required(login_url='SigninPage')
def ViewRetailsOrderItemsPage(request, id):
    OrderId = RetailsOrder.objects.get(id=id)


    queryset = RetailsOrderItems.objects.filter(
                order__id__icontains = OrderId.id
                )

    get_sum = RetailsOrderItems.objects.filter(
        order__id__icontains = OrderId.id
        ).aggregate(sum=Sum('price'))

    # queryset = RetailsOrderItems.objects.all(
                
    #             )
    context = {
        "queryset": queryset,
        "OrderId": OrderId,
        "get_sum":get_sum,
        
    }
    

    return render(request, 'RetailsTemplatesApp/ViewRetailsOrderItemsPage.html',context)












#-----------------Retails DRINKS ORDERS------------------

@login_required(login_url='SigninPage')
def RetailsDrinksOrderPage(request):
    queryset = RetailsDrinksOrder.objects.all().order_by('-id')
    # Calculate the main total price for all orders
    main_total_price = queryset.aggregate(Sum('total_price'))['total_price__sum']
    print(main_total_price);
    get_sum = 0
    get_sum_filter_date = 0
    start_date = 0
    end_date = 0
    username = 0

    

    

    form = RetailsDrinksOrderSearchForm(request.POST or None)
    

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


            
            queryset = RetailsDrinksOrder.objects.all().order_by('-id')
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
            
            queryset = RetailsDrinksOrder.objects.all().order_by('-id')
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

            queryset = RetailsDrinksOrder.objects.filter(
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


    return render(request, 'RetailsTemplatesApp/RetailsDrinksOrderPage.html', context)








@login_required(login_url='SigninPage')
def DeleteRetailsDrinksOrder(request,id):
    x = RetailsDrinksOrder.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Order was deleted Successfully")
    return redirect('RetailsDrinksOrderPage')












#-------------------VIEW Retails Drinks ORDER ITEMS-----------------------

@login_required(login_url='SigninPage')
def ViewRetailsDrinksOrderItemsPage(request, id):
    OrderId = RetailsDrinksOrder.objects.get(id=id)


    queryset = RetailsDrinksOrderItems.objects.filter(
                order__id__icontains = OrderId.id
                )

    get_sum = RetailsDrinksOrderItems.objects.filter(
        order__id__icontains = OrderId.id
        ).aggregate(sum=Sum('price'))

    # queryset = RetailsDrinksOrderItems.objects.all(
                
    #             )
    context = {
        "queryset": queryset,
        "OrderId": OrderId,
        "get_sum":get_sum,
        
    }
    

    return render(request, 'RetailsTemplatesApp/ViewRetailsDrinksOrderItemsPage.html',context)














#----------------Retails ROOMS ORDERS----------------------------

@login_required(login_url='SigninPage')
def RetailsRoomsOrderPage(request):
    queryset = RetailsRoomsOrder.objects.all().order_by('-id')
    # Calculate the main total price for all orders
    main_total_price = queryset.aggregate(Sum('total_price'))['total_price__sum']
    print(main_total_price);
    get_sum = 0
    get_sum_filter_date = 0
    start_date = 0
    end_date = 0
    username = 0

    

    

    form = RetailsRoomsOrderSearchForm(request.POST or None)
    

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


            
            queryset = RetailsRoomsOrder.objects.all().order_by('-id')
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
            
            queryset = RetailsRoomsOrder.objects.all().order_by('-id')
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

            queryset = RetailsRoomsOrder.objects.filter(
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


    return render(request, 'RetailsTemplatesApp/RetailsRoomsOrderPage.html', context)








@login_required(login_url='SigninPage')
def DeleteRetailsRoomsOrder(request,id):
    x = RetailsRoomsOrder.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Order was deleted Successfully")
    return redirect('RetailsRoomsOrderPage')












#-------------------VIEW Retails Rooms ORDER ITEMS-----------------------

@login_required(login_url='SigninPage')
def ViewRetailsRoomsOrderItemsPage(request, id):
    OrderId = RetailsRoomsOrder.objects.get(id=id)


    queryset = RetailsRoomsOrderItems.objects.filter(
                order__id__icontains = OrderId.id
                )

    get_sum = RetailsRoomsOrderItems.objects.filter(
        order__id__icontains = OrderId.id
        ).aggregate(sum=Sum('price'))

    # queryset = RetailsRoomsOrderItems.objects.all(
                
    #             )
    context = {
        "queryset": queryset,
        "OrderId": OrderId,
        "get_sum":get_sum,
        
    }
    

    return render(request, 'RetailsTemplatesApp/ViewRetailsRoomsOrderItemsPage.html',context)



























#-----------------------Retails STAFF MAINTENANCE-----------------


#-------------------Retails STAFFS--------------------------------


@login_required(login_url='SigninPage')
def RetailsMyUserPage(request):
    queryset = MyUser.objects.filter(is_retails_user=True).order_by('id')
    form = RetailsMyUserSearchForm(request.POST or None)

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

    return render(request, 'RetailsTemplatesApp/RetailsMyUserPage.html', context)


@login_required(login_url='SigninPage')
def Retails_search_username_RetailsMyUser_autocomplete(request):
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
def Retails_search_email_RetailsMyUser_autocomplete(request):
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
def DeleteRetailsMyUser(request,id):
    x = MyUser.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Staff was deleted Successfully")
    return redirect('RetailsMyUserPage')




















#-----------------Retails  SUPPLIER---------------------------


@login_required(login_url='SigninPage')
def RetailsSuppliersPage(request):
    queryset = RetailsSuppliers.objects.all().order_by('-id')

    form = RetailsSuppliersSearchForm(request.POST or None)

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
                        

            queryset = RetailsSuppliers.objects.filter(query)
    

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

            

                                            
    #         queryset = RetailsSuppliers.objects.filter(
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
    #             queryset = RetailsSuppliers.objects.all().order_by('-id')
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

    return render(request, 'RetailsTemplatesApp/RetailsSuppliersPage.html', context)





@login_required(login_url='SigninPage')
def Retails_search_SupplierFullName_RetailsSuppliers_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(SupplierFullName__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = RetailsSuppliers.objects.filter(search)
    mylist= []
    mylist += [x.SupplierFullName for x in queryset]
    return JsonResponse(mylist, safe=False)


@login_required(login_url='SigninPage')
def Retails_search_Keyword_RetailsSuppliers_autocomplete(request):
    print(request.GET)
    #form = AvailableMedicinesForm()
    query_original = request.GET.get('term')
    search = Q(Keyword__icontains=query_original)
    #queryset = Dozi.objects.filter(name__icontains=query_original)
    queryset = RetailsSuppliers.objects.filter(search)
    mylist= []
    mylist += [x.Keyword for x in queryset]
    return JsonResponse(mylist, safe=False)



@login_required(login_url='SigninPage')
def DeleteRetailsSuppliers(request,id):
    x = RetailsSuppliers.objects.get(id=id)
        
    x.delete()
    messages.success(request,f"Supplier was deleted Successfully")
    return redirect('RetailsSuppliersPage')



@login_required(login_url='SigninPage')
def AddRetailsSuppliers(request):
    
    form = AddRetailsSuppliersForm()
    
    if request.method == "POST":
        form=AddRetailsSuppliersForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data Added Successfully")
            return redirect('RetailsSuppliersPage')

        messages.success(request,f"Failed to add new data")
        return redirect('AddRetailsSuppliers')


    context = {
        "form":form,
        

    }
    
    return render(request, 'RetailsAddPage/AddRetailsSuppliers.html', context)



@login_required(login_url='SigninPage')
def UpdateRetailsSuppliers(request,id):
    x = RetailsSuppliers.objects.get(id=id)
    form = AddRetailsSuppliersForm(instance=x)
    
    if request.method == "POST":
        form=AddRetailsSuppliersForm(request.POST or None, files=request.FILES, instance=x)
        if form.is_valid():
            form.save()
            messages.success(request,f"Data updated Successfully")
            return redirect('RetailsSuppliersPage')

    context = {
        "form":form,
        "x":x,

    }
    
    return render(request, 'RetailsUpdatePage/UpdateRetailsSuppliers.html', context)











#---------------UPLOAD PRODUCTS----------------------




#--------------UPLOAD FOOD PRODUCTS--------------------
def UploadRetailsProductsPage(request):
    if request.method == "POST":
        item_resource = RetailsProductsResource()
        dataset = Dataset()
        new_item_resource = request.FILES['myfile']

        if not new_item_resource.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request, 'RetailsAddPage/UploadRetailsProductsPage.html')


        imported_data = dataset.load(new_item_resource.read(), format='xlsx')

        for data in imported_data:
            value = RetailsProducts(
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
    return render(request, 'RetailsAddPage/UploadRetailsProductsPage.html')



    #return HttpResponse("File Uploaded Successfully")









#--------------UPLOAD DRINKS PRODUCTS--------------------
def UploadRetailsDrinksProductsPage(request):
    if request.method == "POST":
        item_resource = RetailsDrinksProductsResource()
        dataset = Dataset()
        new_item_resource = request.FILES['myfile']

        if not new_item_resource.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return render(request, 'RetailsAddPage/UploadRetailsDrinksProductsPage.html')


        imported_data = dataset.load(new_item_resource.read(), format='xlsx')

        for data in imported_data:
            value = RetailsDrinksProducts(
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
    return render(request, 'RetailsAddPage/UploadRetailsDrinksProductsPage.html')



    #return HttpResponse("File Uploaded Successfully")








