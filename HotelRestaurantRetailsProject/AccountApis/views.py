from django.shortcuts import render,redirect


# Create your views here.
from django.shortcuts import render,get_object_or_404
from HotelApis.serializers import *
from HotelApis.models import *
from .serializers import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages


#REST FRAMEWORK
from rest_framework import status
from rest_framework.response import Response

#---------------------FUNCTION VIEW-------------------------
from rest_framework.decorators import api_view

#------------------------CLASS BASED VIEW-------------------
from rest_framework.views import APIView


#------------------------GENERIC VIEWs-------------------
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView


#------------------------ VIEW SETS-------------------
from rest_framework.viewsets import ModelViewSet


#------FILTERS, SEARCH AND ORDERING
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter,OrderingFilter

#------PAGINATION-------------
from rest_framework.pagination import PageNumberPagination




#----------------CREATING A CART------------------------
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from HotelApis.serializers import *
from drf_yasg.utils import swagger_auto_schema

from rest_framework import generics,status
from rest_framework.decorators import api_view

# Create your views here.

# class UserView(APIView):

#   def get(self,request, format=None):
#       return Response("User Account View", status=200)

#   def post(self,request, format=None):

#       return Response("Creating User", status=200)



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView



import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed










#-----------------------------------------------


from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from HotelApis.models import MyUser  # Make sure to import your MyUser model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# class RegistrationView(generics.CreateAPIView):
#     queryset = MyUser.objects.all()
#     serializer_class = DjangoReactUserSerializer
#     permission_classes = (permissions.AllowAny,)

# class ReactLoginView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = DjangoReactUserSerializer
    
#     def create(self, request, *args, **kwargs):
#         user = self.get_object()
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})


from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import authentication_classes, permission_classes
from .authentication import ExpiringTokenAuhtentication


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings

from .forms import *

# class CustomerAuthTokenLogin(ObtainAuthToken):
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             data=request.data,
#             context={'request':request}
#             )
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']

#         utc_now = datetime.datetime.utcnow()
#         utc_now =utc_now.replace(tzinfo = pytz.utc)

#         result = Token.objects.filter(user=user, created__lt = utc_now - datetime.timedelta(seconds=30)).delete()

#         token, created = Token.objects.get_or_create(user=user)


#         return Response({
#             'token':token.key,
#             'user_id':user.pk,
#             'username':user.username
#             })





#--------------MWANZO WA RESET PASSWORD-----------------


class PasswordReset(generics.GenericAPIView):
    """
    Request for Password Reset Link.
    """

    serializer_class = EmailSerializer

    def post(self, request):
        """
        Create token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = MyUser.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse(
                "reset-password",
                kwargs={"encoded_pk": encoded_pk, "token": token},
            )
            reset_link = f"localhost:8000{reset_url}"

            #Send Reset Link to the Email
            #username = request.POST.get('email')
            #last_name = request.POST['last_name']
            email = request.data.get('email')
            subject = "Easy-Fix"
            message =  f"To reset change the password click this link: {reset_link} "
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=True)







            # send the rest_link as mail to the user.

            return Response(
                {
                    "message": 
                    f"Your password rest link: {reset_link}"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ResetPasswordAPI(generics.GenericAPIView):
    """
    Verify and Reset Password Token View.
    """

    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        """
        Verify token & encoded_pk and then reset the password.
        """
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )







#--------------MWISHO WA RESET PASSWORD-----------------









class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            username = serializer.validated_data.get('username')
            #phone = serializer.validated_data.get('phone')
            # last_name = serializer.validated_data.get('last_name')
            
            if MyUser.objects.filter(email=email).exists():
                return Response({'error': 'email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = MyUser.objects.create_user(email=email, password=password, username=username)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Registration failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReactLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)





class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            Token.objects.filter(user=user).delete()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)





class UserDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        # Assuming you have a serializer for User data
        serializer = UserDataSerializer(user)
        return Response(serializer.data)



















#---------------ADMIN HOME PAGE--------------

def AdminHomePage(request):

    return render(request, "Account/AdminHomePage.html")

#---------REGISTER NEW USER BY ADMIN-------------
def RegisterNewUserByAdmin(request):
    if request.method == "POST":
        form = RegisterNewUserByAdminMyUserForm(request.POST)
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
            return redirect('RegisterNewUserByAdmin')
    else:
        form = RegisterNewUserByAdminMyUserForm()

    context = {
        "form": form
    }
    return render(request, 'Account/RegisterNewUserByAdmin.html', context)



