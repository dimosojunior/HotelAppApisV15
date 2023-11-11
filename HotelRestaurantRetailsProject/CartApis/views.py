from django.shortcuts import render
from django.shortcuts import render,redirect

from django.http import HttpResponse
# Create your views here.
from django.shortcuts import render,get_object_or_404
from HotelApis.serializers import *
from HotelApis.models import *
from HotelApis.serializers import *
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.db import transaction
from .serializers import *

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
from RestaurantApis.serializers import *
from RetailsApis.serializers import *
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

from rest_framework.pagination import PageNumberPagination
# Create your views here.





#ORDER PAGINATION-------------------------
#http://127.0.0.1:8000/Cart/HotelOrder/?page=1&page_size=1





def HomeView(request):

    return HttpResponse("CART APIS")

#GET /your-api-endpoint/?page=2&page_size=5

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 1  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 100


#---------------HOTEL CART  APIS--------------------------

# Eg:
# {
#     "product":1,
#     "quantity":1,
#     "CustomerFullName":"dimoso junior",
#     "PhoneNumber":"0765456743",
#     "CustomerAddress":"magomeni",
#     "room":1,
#     "table":1
# }
    
    



class HotelCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = HotelCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelCartItems.objects.filter(cart=cart)
        serializer = HotelCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)

    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelCart.objects.get_or_create(user=user, ordered=False)
        product = HotelProducts.objects.get(id=data.get('product'))

        # room = HotelRooms.objects.get(id=data.get('room'))
        # table = HotelTables.objects.get(id=data.get('table'))
        # Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = HotelCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = HotelCartItems.objects.get(id=data.get('cartId'))
        cart_item.delete()

        cart = HotelCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelCartItems.objects.filter(cart=cart)
        serializer = HotelCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class HotelDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = HotelCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except HotelCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class HotelOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = HotelCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = HotelOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = HotelCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create HotelOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = HotelOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create HotelOrderItems instances for better performance
    #     HotelOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(HotelOrderSerializer(order).data, status=status.HTTP_201_CREATED)



    #----------------MAKE ORDER  WITHOUT ROOM --------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)
        cart = HotelCart.objects.filter(user=user, ordered=False).first()
        table = HotelTables.objects.get(id=data.get('table'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Inventory product category ID from the cart items
        product_category_ids = set()  # Using a set to ensure unique category IDs
        cart_items = HotelCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            product_category_ids.add(cart_item.product.productCategory.Inventory.id)

        # Create the order
        order = HotelOrder.objects.create(user=user, total_price=total_price, table_number=table.TableNumber)
        
        # Assign the first category ID found to the Order CategoryId field
        if product_category_ids:
            order.CategoryId = product_category_ids.pop()
            order.save()

        total_cart_items = HotelCartItems.objects.filter(user=user)
        total_price = sum(items.price for items in total_cart_items)
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Create order items
        for cart_item in cart_items:
            HotelOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                price=cart_item.price,
                quantity=cart_item.quantity,
                table=table
            )

        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOrder.objects.all().order_by('-id')
            orders = HotelOrder.objects.filter(
                user=user,
                room_number = None
                ).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#---------MAKE ORDER WITH ROOM FIELD
class MakeHotelOrderWithRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelCart.objects.filter(user=user, ordered=False).first()

        room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        order = HotelOrder.objects.create(user=user, total_price=total_price, table_number=table.TableNumber,room_number=room.RoomName)

        total_cart_items = HotelCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Update the table status to True
        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelOrderSerializer(order).data, status=status.HTTP_201_CREATED)




#NOW NATUMIA HII FOR HOTEL GUEST NA SIYO HIYO YA JUU

#TO ADD ROOM ORDER TO ORDERED  ITEMS
class PlusRoom_MakeHotelOrderWithRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data

        # Get the customer based on customer_id from the request data
        customer_id = data.get('Customer')
        customer = HotelCustomers.objects.get(id=customer_id)

        # Check if the customer has booked a room
        has_booked_room = HotelRoomsOrderItems.objects.filter(
            Customer=customer,
            is_customer_opened_closed=False
            ).exists()

        total_price = request.data.get('total_price', 0)

        pending_total_price = request.data.get('pending_total_price', 0)
        true_total_price = request.data.get('true_total_price', 0)

        cart = HotelCart.objects.filter(user=user, ordered=False).first()

        room = HotelRooms.objects.get(id=data.get('room'))
        table = HotelTables.objects.get(id=data.get('table'))



        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        
        # Fetch the Inventory product category ID from the cart items
        product_category_ids = set()  # Using a set to ensure unique category IDs
        cart_items = HotelCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            product_category_ids.add(cart_item.product.productCategory.Inventory.id)


        # Calculate the total price of  items
        total_cart_items = HotelCartItems.objects.filter(user=user)
        total__price = sum(item.price for item in total_cart_items)

        # If the customer has booked a room, include the room price in the total
        if has_booked_room:
            room_order = HotelRoomsOrderItems.objects.filter(Customer=customer).first()
            room_price = room_order.order.total_price

            
            total_price = total__price + room_price
            #hapa utapata anayotakiwa kulipa kwenye room tu
            pending_total_price = total_price-total__price
            #hapa utapata anayotakiwa kulipa kwenye  tu
            true_total_price = total_price-room_price

            # Create an order
            order = HotelOrder.objects.create(
            user=user, 
            total_price=total_price,
            pending_total_price=pending_total_price,
            true_total_price=true_total_price,

            #copy room number and table number to HotelOrder Fields 
            table_number=table.TableNumber,
            room_number=room.RoomName,

            number_of_days=room_order.DaysNumber,
            room_price=room.price
            )  # Set the table_number here

            # Assign the first category ID found to the Order CategoryId field
            if product_category_ids:
                order.CategoryId = product_category_ids.pop()
                order.save()
            
        else:
            total_price = total__price

            # Create an order
            order = HotelOrder.objects.create(
            user=user, 
            total_price=total_price,
            pending_total_price=pending_total_price,
            true_total_price=true_total_price,

            #copy room number and table number to HotelOrder Fields 
            table_number=table.TableNumber,
            room_number=room.RoomName,

            #number_of_days=room_order.DaysNumber,
            room_price=room.price
            )  # Set the table_number here

            # Assign the first category ID found to the Order CategoryId field
            if product_category_ids:
                order.CategoryId = product_category_ids.pop()
                order.save()


        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = HotelCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            HotelOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                price=cart_item.price,
                quantity=cart_item.quantity,
                room=room,
                table=table,
                Customer=customer
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(HotelOrderSerializer(order).data, status=status.HTTP_201_CREATED)







#-------------------ADD TO CART AND MAKE ORDER WITHOUT ROOM

class HotelAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelCart.objects.get_or_create(user=user, ordered=False)
        product = HotelProducts.objects.get(id=data.get('product'))
        # Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        
        #table = HotelTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity 
            # table=table,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = HotelCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})











#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class HotelOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = HotelOrder.objects.create(user=user, total_price=total_price)

        cart_items = HotelCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = HotelCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(HotelOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = HotelOrder.objects.filter(user=user)
        serializer = HotelOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)





























































#---------------HOTEL CART ROOMS APIS--------------------------


# ADD ROOM TO THE CART
#  {
#      "room":3,
#      "quantity":1,
#      "CustomerFullName":"saidi abdallah",
#      "PhoneNumber":"+25567534562",
#      "CustomerAddress":"iyunga",
#      "DaysNumber":3,
#       "table":1


#  }


class HotelRoomsCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelRoomsCartItems.objects.filter(cart=cart)
        serializer = HotelRoomsCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = HotelRoomsCart.objects.get_or_create(user=user, ordered=False)
        room = HotelRooms.objects.get(id=data.get('room'))
        # Customer = HotelCustomers.objects.get(id=data.get('Customer'))
        #table = HotelTables.objects.get(id=data.get('table'))
        price = room.price
        #quantity = data.get('quantity')
        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')
        DaysNumber = data.get('DaysNumber')

        # Check if the requested quantity is available in stock
        if room.ProductQuantity != 1:
            return Response({'error': 'This room has not available'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = HotelRoomsCartItems(
            cart=cart,
             user=user,
             room=room,
             price=price,
             #Customer=Customer,
             # CustomerFullName=CustomerFullName,
             # PhoneNumber=PhoneNumber,
             # CustomerAddress=CustomerAddress,
             DaysNumber=DaysNumber
             )
        cart_items.save()

        # Decrease the room quantity in stock
        room.ProductQuantity -= 1
        room.save()

        cart_items = HotelRoomsCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = HotelRoomsCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = HotelRoomsCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()
        queryset = HotelRoomsCartItems.objects.filter(cart=cart)
        serializer = HotelRoomsCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class HotelRoomsDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = HotelRoomsCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.room.ProductQuantity += cart_item.quantity
            cart_item.room.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsCartItems.DoesNotExist:
            return Response({"error": "Room not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class HotelRoomsOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    # def post(self, request):
    #     user = request.user
    #     data = request.data

    #     CustomerFullName = data.get('CustomerFullName')
    #     PhoneNumber = data.get('PhoneNumber')
    #     CustomerAddress = data.get('CustomerAddress')
    #     DaysNumber = data.get('DaysNumber')

    #     total_price = request.data.get('total_price', 0)  # You may calculate this on the server
    #     cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     with transaction.atomic():  # Use a transaction to ensure data consistency

    #         order = HotelRoomsOrder.objects.create(user=user, total_price=total_price)

    #         total_cart_items = HotelRoomsCartItems.objects.filter(user=user)

    #         total_price = 0
    #         for items in total_cart_items:
    #             total_price += items.price
    #         order.total_price = total_price
    #         order.save()

    #         # Retrieve cart items and add them to the order
    #         cart_items = HotelRoomsCartItems.objects.filter(user=user, cart=cart)
            

    #         order_items = []
    #         for cart_item in total_cart_items:
                
    #             order_item = HotelRoomsOrderItems(
    #                 user=user,
    #                 order=order,
    #                 room=cart_item.room,
    #                 price=cart_item.price,
    #                 quantity=cart_item.quantity,
    #                 CustomerFullName=cart_item.CustomerFullName,
    #                 PhoneNumber=cart_item.PhoneNumber,
    #                 CustomerAddress=cart_item.CustomerAddress,
    #                 DaysNumber=cart_item.DaysNumber
    #             )
    #             order_items.append(order_item)

    #         # Bulk create HotelDrinksOrderItems instances for better performance
    #         HotelRoomsOrderItems.objects.bulk_create(order_items)

    #         # Add the cart items to the order's ManyToManyField
    #         order.orderItems.set(order_items)


    #         # Update RoomStatus to True for ordered rooms
    #         for cart_item in cart_items:
    #             cart_item.room.RoomStatus = True
    #             cart_item.room.save()

    #         # Clear the user's cart
    #         cart_items.delete()
    #         cart.total_price = 0
    #         cart.ordered = True
    #         cart.save()




    #     return Response(HotelRoomsOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    def post(self, request):
        user = request.user
        data = request.data

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        #room = HotelRooms.objects.get(id=data.get('room'))
        Customer = HotelCustomers.objects.get(id=data.get('Customer'))

        DaysNumber = data.get('DaysNumber')

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = HotelRoomsCart.objects.filter(user=user, ordered=False).first()

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Create an order
        with transaction.atomic():  # Use a transaction to ensure data consistency

            order = HotelRoomsOrder.objects.create(user=user, total_price=total_price)

            total_cart_items = HotelRoomsCartItems.objects.filter(user=user)

            total_price = 0
            for items in total_cart_items:
                total_price += items.price
            order.total_price = total_price
            order.save()

            # Retrieve cart items and add them to the order
            cart_items = HotelRoomsCartItems.objects.filter(user=user, cart=cart)
            for cart_item in cart_items:
                HotelRoomsOrderItems.objects.create(
                    user=user,
                    order=order,
                    room=cart_item.room,
                    price=cart_item.price,
                    quantity=cart_item.quantity,
                    # Customer=cart_item.Customer,
                    # CustomerFullName=cart_item.CustomerFullName,
                    # PhoneNumber=cart_item.PhoneNumber,
                    # CustomerAddress=cart_item.CustomerAddress,
                    Customer=Customer,
                    DaysNumber=cart_item.DaysNumber,
                    is_customer_opened_closed=False
                )


            # Update RoomStatus to True for ordered rooms
            for cart_item in cart_items:
                cart_item.room.RoomStatus = True
                cart_item.room.save()

            # Clear the user's cart
            cart_items.delete()
            cart.total_price = 0
            cart.ordered = True
            cart.save()




        return Response(HotelRoomsOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = HotelRoomsOrder.objects.filter(user=user)
    #     serializer = HotelRoomsOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOrder.objects.all().order_by('-id')
            orders = HotelRoomsOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelRoomsOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




































#------------------------RESTAURANT CARTS ZINAANZIA HAPA--------------







#---------------Restaurant CART  APIS--------------------------




class RestaurantCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RestaurantCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantCartItems.objects.filter(cart=cart)
        serializer = RestaurantCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantProducts.objects.get(id=data.get('product'))

        # room = RestaurantRooms.objects.get(id=data.get('room'))
        # table = RestaurantTables.objects.get(id=data.get('table'))
        # Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RestaurantCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RestaurantCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RestaurantCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RestaurantCart.objects.filter(user=user, ordered=False).first()
        queryset = RestaurantCartItems.objects.filter(cart=cart)
        serializer = RestaurantCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RestaurantDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RestaurantCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RestaurantCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RestaurantOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RestaurantCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RestaurantOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RestaurantCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RestaurantOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RestaurantOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RestaurantOrderItems instances for better performance
    #     RestaurantOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RestaurantOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    #----------------MAKE ORDER  WITHOUT ROOM AND TABLE--------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RestaurantCart.objects.filter(user=user, ordered=False).first()

        #room = RestaurantRooms.objects.get(id=data.get('room'))
        table = RestaurantTables.objects.get(id=data.get('table'))
        Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Inventory product category ID from the cart items
        product_category_ids = set()  # Using a set to ensure unique category IDs
        cart_items = RestaurantCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            product_category_ids.add(cart_item.product.productCategory.Inventory.id)

        # Create the order
        order = RestaurantOrder.objects.create(user=user, total_price=total_price, table_number=table.TableNumber)
        
        # Assign the first category ID found to the Order CategoryId field
        if product_category_ids:
            order.CategoryId = product_category_ids.pop()
            order.save()

        total_cart_items = RestaurantCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = RestaurantCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RestaurantOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RestaurantOrderSerializer(order).data, status=status.HTTP_201_CREATED)

    # def get(self, request):
    #     user = request.user
    #     orders = RestaurantOrder.objects.filter(user=user)
    #     serializer = RestaurantOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOrder.objects.all().order_by('-id')
            orders = RestaurantOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RestaurantOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RestaurantOrder.objects.create(user=user, total_price=total_price)

        cart_items = RestaurantCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RestaurantCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RestaurantOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RestaurantOrder.objects.filter(user=user)
        serializer = RestaurantOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RestaurantAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RestaurantCart.objects.get_or_create(user=user, ordered=False)
        product = RestaurantProducts.objects.get(id=data.get('product'))
        Customer = RestaurantCustomers.objects.get(id=data.get('Customer'))

        
        table = RestaurantTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RestaurantCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RestaurantCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})


































#RESTAURANTS CART ZINAISHIA HAPA-------------------------------







































#---------------------------RETAILS CART ZINAANZIA HAPA----------------












#---------------Retails CART  APIS--------------------------




class RetailsCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # kama unatumia JWT weka hiyo tu
    # permission_classes =[IsAuthenticated]

#RETRIEVE CART ITEMS FROM A CART
    def get(self, request):
        user = request.user
        cart = RetailsCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsCartItems.objects.filter(cart=cart)
        serializer = RetailsCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)


    #ADD ITEM TO THE CART WITHOUT ROOM FIELD
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsProducts.objects.get(id=data.get('product'))

        # room = RetailsRooms.objects.get(id=data.get('room'))
        # table = RetailsTables.objects.get(id=data.get('table'))
        # Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        price = product.price
        quantity = data.get('quantity')

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity,
            # table=table,
            # room=room,
            # Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})



    #TO UPDATE CART ITEMS
    #Eg:
    # {
    #     "id":11,
    #     "quantity":6
    # }
    def put(self, request):
        data = request.data
        cart_item = RetailsCartItems.objects.get(id=data.get('id'))
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({'success': 'Item Updated Sccussfully'})



    #TO DELETE ITEM IN A CART
    #Eg:
    #Pass id of the product
    # {
    #     "id":9

    # }
    def delete(self, request):
        user = request.user
        data = request.data
        cart_item = RetailsCartItems.objects.get(id=data.get('id'))
        cart_item.delete()

        cart = RetailsCart.objects.filter(user=user, ordered=False).first()
        queryset = RetailsCartItems.objects.filter(cart=cart)
        serializer = RetailsCartItemsSerializer(queryset, many=True)

        return Response(serializer.data)





class RetailsDeleteCartItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            cart_item = RetailsCartItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            cart_item.product.ProductQuantity += cart_item.quantity
            cart_item.product.save()

            cart_item.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except RetailsCartItems.DoesNotExist:
            return Response({"error": "Product not found in the cart"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# Enter id of the Cart
# Eg:
# {
#     "id":2

# }

#AFTER MAKING ORDER IF YOU WANT TO DELETE A CART ITEMS USE THIS
class RetailsOrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def post(self, request):
    #     user = request.user
    #     total_price = request.data.get('total_price', 0)
    #     cart = RetailsCart.objects.filter(user=user, ordered=False).first()

    #     if not cart:
    #         return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

    #     # Create an order
    #     order = RetailsOrder.objects.create(user=user, total_price=total_price)

    #     total_cart_items = RetailsCartItems.objects.filter(user=user)

    #     total_price = 0
    #     for items in total_cart_items:
    #         total_price += items.price
    #     order.total_price = total_price
    #     order.save()

    #     # Create RetailsOrderItems instances and calculate total price
    #     order_items = []
    #     for cart_item in total_cart_items:
            
    #         order_item = RetailsOrderItems(
    #             user=user,
    #             order=order,
    #             product=cart_item.product,
    #             price=cart_item.price,
    #             quantity=cart_item.quantity
    #         )
    #         order_items.append(order_item)

    #     # Bulk create RetailsOrderItems instances for better performance
    #     RetailsOrderItems.objects.bulk_create(order_items)

    #     # Add the cart items to the order's ManyToManyField
    #     order.orderItems.set(order_items)

    #     # Clear the user's cart
    #     total_cart_items.delete()
    #     cart.total_price = 0
    #     cart.ordered = True
    #     cart.save()

    #     return Response(RetailsOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    #----------------MAKE ORDER  WITHOUT ROOM AND TABLE--------------------
    def post(self, request):
        user = request.user
        data = request.data

        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        cart = RetailsCart.objects.filter(user=user, ordered=False).first()

        #room = RetailsRooms.objects.get(id=data.get('room'))
        table = RetailsTables.objects.get(id=data.get('table'))
        Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        if not cart:
            return Response({'error': 'No items in the cart'}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch the Inventory product category ID from the cart items
        product_category_ids = set()  # Using a set to ensure unique category IDs
        cart_items = RetailsCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            product_category_ids.add(cart_item.product.productCategory.Inventory.id)

        # Create the order
        order = RetailsOrder.objects.create(user=user, total_price=total_price, table_number=table.TableNumber)
        
        # Assign the first category ID found to the Order CategoryId field
        if product_category_ids:
            order.CategoryId = product_category_ids.pop()
            order.save()
            
        total_cart_items = RetailsCartItems.objects.filter(user=user)

        total_price = 0
        for items in total_cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        table.TableStatus = True
        table.save()

        # Retrieve cart items and add them to the order
        cart_items = RetailsCartItems.objects.filter(user=user, cart=cart)
        for cart_item in cart_items:
            RetailsOrderItems.objects.create(
                user=user,
                order=order,
                product=cart_item.product,
                
                price=cart_item.price,
                quantity=cart_item.quantity,

                #room=room,
                table=table,
                Customer=Customer
                # CustomerFullName=cart_item.CustomerFullName,
                # CustomerAddress=cart_item.CustomerAddress,
                # PhoneNumber=cart_item.PhoneNumber
            )

        # Clear the user's cart
        cart_items.delete()
        cart.total_price = 0
        cart.ordered = True
        cart.save()

        return Response(RetailsOrderSerializer(order).data, status=status.HTTP_201_CREATED)


    # def get(self, request):
    #     user = request.user
    #     orders = RetailsOrder.objects.filter(user=user)
    #     serializer = RetailsOrderSerializer(orders, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOrder.objects.all().order_by('-id')
            orders = RetailsOrder.objects.filter(user=user).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





#AFTER MAKING ORDER IF YOU DON'T WANT TO DELETE A CART ITEMS USE THIS
class RetailsOrdernNoDeleteView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # Create a new order
    def post(self, request):
        user = request.user
        total_price = request.data.get('total_price', 0)  # You may calculate this on the server
        order = RetailsOrder.objects.create(user=user, total_price=total_price)

        cart_items = RetailsCartItems.objects.filter(user=user)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        order.total_price = total_price
        order.save()

        # Clear the user's cart
        # cart_items.delete()
        # cart = RetailsCart.objects.get(user=user, ordered=False)
        # cart.total_price = 0
        # cart.save()

        return Response(RetailsOrderSerializer(order).data, status=status.HTTP_201_CREATED)
        #return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = request.user
        orders = RetailsOrder.objects.filter(user=user)
        serializer = RetailsOrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    



#------------------ADD ITEMS TO THE CART WITHOUT ROOM
class RetailsAddToCartWithoutRoomView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        cart, _ = RetailsCart.objects.get_or_create(user=user, ordered=False)
        product = RetailsProducts.objects.get(id=data.get('product'))
        Customer = RetailsCustomers.objects.get(id=data.get('Customer'))

        
        table = RetailsTables.objects.get(id=data.get('table'))

        # CustomerFullName = data.get('CustomerFullName')
        # PhoneNumber = data.get('PhoneNumber')
        # CustomerAddress = data.get('CustomerAddress')

        price = product.price
        quantity = data.get('quantity')

        # Check if the requested quantity is available in stock
        if product.ProductQuantity < quantity:
            return Response({'error': 'Not enough quantity in stock'}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = RetailsCartItems(
            cart=cart, 
            user=user, 
            product=product, 
            price=price, 
            quantity=quantity, 
            table=table,
            Customer=Customer
            # CustomerFullName=CustomerFullName,
            # PhoneNumber=PhoneNumber,
            # CustomerAddress=CustomerAddress
            )
        cart_items.save()

        # Decrease the product quantity in stock
        product.ProductQuantity -= quantity
        product.save()

        cart_items = RetailsCartItems.objects.filter(user=user, cart=cart.id)

        total_price = 0
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success': 'Items Added To Your Cart'})






















































#-----------------REPORT------------------------------------------


#------------HOTEL  REPORT--------------------------



#TO GET ORDER ITEMS WITHOUT PAGINATION
# class HotelOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = HotelOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = HotelOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class HotelOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = HotelOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = HotelOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class HotelOrderReportView(APIView):
#     def get(self, request):
#         orders = HotelOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = HotelOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class HotelOrderReportView(APIView):
    #-------------TO GET ALL ORDERS WITH PAGINATION
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = HotelOrder.objects.all().order_by('-id')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = HotelOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)

    #FOR WALKING CUSTOMER ONLY
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))
            CategoryId = int(request.query_params.get('CategoryId'))

            orders = HotelOrder.objects.filter(
                user__id__icontains = userId,
                room_number = None,
                CategoryId=CategoryId


                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







































#------------HOTEL Rooms REPORT--------------------------


#TO GET ORDER ITEMS WITHOUT PAGINATION
# class HotelRoomsOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = HotelRoomsOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = HotelRoomsOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class HotelRoomsOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = HotelRoomsOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = HotelRoomsOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class HotelRoomsOrderReportView(APIView):
#     def get(self, request):
#         orders = HotelRoomsOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = HotelRoomsOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION

class HotelRoomsOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = HotelRoomsOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = HotelRoomsOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelRoomsOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))
            CategoryId = int(request.query_params.get('CategoryId'))

            orders = HotelRoomsOrder.objects.filter(
                user__id__icontains = userId,
                CategoryId=CategoryId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelRoomsOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

























#------------Restaurant  REPORT--------------------------







#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RestaurantOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RestaurantOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RestaurantOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RestaurantOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RestaurantOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RestaurantOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RestaurantOrderReportView(APIView):
#     def get(self, request):
#         orders = RestaurantOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RestaurantOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class RestaurantOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RestaurantOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RestaurantOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RestaurantOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))
            CategoryId = int(request.query_params.get('CategoryId'))

            orders = RestaurantOrder.objects.filter(
                user__id__icontains = userId,
                CategoryId=CategoryId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RestaurantOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
























#------------Retails  REPORT--------------------------



#TO GET ORDER ITEMS WITHOUT PAGINATION
# class RetailsOrderReportView(APIView):
#     def get(self, request):
#         try:
#             orders = RetailsOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             #main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             serializer = RetailsOrderItemsSerializer(orders, many=True)

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 #'main_total_price': main_total_price
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



#TO GET ORDER ITEMS WITH PAGINATION
from django.db.models import Sum

# class RetailsOrderReportView(APIView):
#     def get(self, request):
#         try:
#             # Get the page number from the query parameters, default to 1
#             page = int(request.query_params.get('page', 1))
#             page_size = int(request.query_params.get('page_size', 2))  # Adjust page size as needed
            
#             orders = RetailsOrderItems.objects.all()

#             # Calculate the main total price for all orders
#             main_total_price = orders.aggregate(Sum('price'))['price__sum']

#             # Use pagination to get the desired page
#             paginator = PageNumberPagination()
#             paginator.page_size = page_size
#             page_items = paginator.paginate_queryset(orders, request)

            
#             serializer = RetailsOrderItemsSerializer(page_items, many=True)
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price,
#                 'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
#                 'current_page': page,  # Send current page info
#             }
                

            

#             # Include the main total price in the response
#             response_data = {
#                 'orders': serializer.data,
#                 'main_total_price': main_total_price
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







#------KAMA ANATAKA KUFILTER ORDERS TUMIA HIII YA CHINI

# TO FILTER ORDERS WITHOUT PAGINATION

# class RetailsOrderReportView(APIView):
#     def get(self, request):
#         orders = RetailsOrder.objects.all()

#         # Calculate the main total price for all orders
#         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

#         serializer = RetailsOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             'orders': serializer.data,
#             'main_total_price': main_total_price
#         }

#         return Response(response_data, status=status.HTTP_200_OK)






#TO FILTER ORDERS WITH PAGINATION


class RetailsOrderReportView(APIView):
    # def get(self, request):
    #     try:
    #         # Get the page number from the query parameters, default to 1
    #         page = int(request.query_params.get('page', 1))
    #         page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            
    #         orders = RetailsOrder.objects.all().order_by('order_status')

    #         # Calculate the main total price for all orders
    #         main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

    #         # Use pagination to get the desired page
            

            
            

    #         paginator = PageNumberPagination()
    #         paginator.page_size = page_size
    #         page_items = paginator.paginate_queryset(orders, request)

    #         serializer = RetailsOrderSerializer(page_items, many=True)

    #         response_data = {
    #             'orders': serializer.data,
    #             'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
    #             'current_page': page,  # Send current page info
    #         }

    #         return Response(response_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    # TO GET ALL ORDERS ORDERED BY SPECIFIC USERS(WAITERS)
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/RetailsOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))
            CategoryId = int(request.query_params.get('CategoryId'))

            orders = RetailsOrder.objects.filter(
                user__id__icontains = userId,
                CategoryId=CategoryId

                ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = RetailsOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


































#------------------FILTER   REPORT--------------------------






#---------------HOTEL FILTER REPORT---------------

#-------------TO FILTER ORDER ITEMS-------------------
# class FilterHotelOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = HotelOrderItems.objects.filter(
#             Created__gte=startDate, Created__lte=endDate
#         )

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("price"))["price__sum"]

#         serializer = HotelOrderItemsSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)





#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterHotelOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = HotelOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = HotelOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterHotelOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterHotelOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))
        CategoryId = int(request.query_params.get('CategoryId'))

        

        # Filter orders based on date range
        orders = HotelOrder.objects.filter(
            user__id__icontains = userId,
            CategoryId=CategoryId,
            room_number = None,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)

















#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterHotelRoomsOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = HotelRoomsOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = HotelRoomsOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterHotelRoomsOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterHotelRoomsOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))
        CategoryId = int(request.query_params.get('CategoryId'))

        

        # Filter orders based on date range
        orders = HotelRoomsOrder.objects.filter(
            user__id__icontains = userId,
            CategoryId=CategoryId,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelRoomsOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)




















#---------------Restaurant FILTER REPORT---------------


#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterRestaurantOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = RestaurantOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = RestaurantOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterRestaurantOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterRestaurantOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))
        CategoryId = int(request.query_params.get('CategoryId'))

        

        # Filter orders based on date range
        orders = RestaurantOrder.objects.filter(
            user__id__icontains = userId,
            CategoryId=CategoryId,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RestaurantOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)
















#---------------RETAILS FILTER REPORT---------------

#---------------------UKITAKA KUFILTER ORDERS ZOTE TUMIA HIII  YA CHINI

# class FilterRetailsOrderReportView(APIView):
#     def get(self, request):
#         startDate = request.query_params.get("startDate") #"2023-09-10"
#         endDate =request.query_params.get("endDate") # "2023-09-30"

#         # Filter orders based on date range
#         orders = RetailsOrder.objects.filter(
#             created__gte=startDate, created__lte=endDate
#         ).order_by('-id')

#         # Calculate the main total price for filtered orders
#         main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

#         serializer = RetailsOrderSerializer(orders, many=True)

#         # Include the main total price in the response
#         response_data = {
#             "orders": serializer.data,
#             "main_total_price": main_total_price,
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


#------------UKITATA KUFILTER ORDER KULINGANA NA USER HUSIKA TUMIA HII
#Eg: http://127.0.0.1:8000/Cart/FilterRetailsOrderReport/?id=2&startDate=2023-09-10&endDate=2023-10-30
class FilterRetailsOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))
        CategoryId = int(request.query_params.get('CategoryId'))

        

        # Filter orders based on date range
        orders = RetailsOrder.objects.filter(
            user__id__icontains = userId,
            CategoryId=CategoryId,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = RetailsOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)










#-----------------RECEIPT ORDER--------------------

#kama untaka order za mda huo tu anapoadd kwenye cart huyo user tumia hii ya chini
# class HotelReceiptView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]
#     # kama unatumia JWT weka hiyo tu
#     # permission_classes =[IsAuthenticated]

# #RETRIEVE CART ITEMS FROM A CART
#     def get(self, request):
#         user = request.user
#         order = HotelOrder.objects.filter(user=user).first()
#         queryset = HotelOrderItems.objects.filter(order=order)
#         serializer = HotelOrderItemsSerializer(queryset, many=True)

#         return Response(serializer.data)


#kama unataka orders zote za huyo users basi tunatumia hii ya chini
class HotelReceiptView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        orders = HotelOrder.objects.filter(user=user)
        order_items = []

        for order in orders:
            queryset = HotelOrderItems.objects.filter(order=order)
            serializer = HotelOrderItemsSerializer(queryset, many=True)
            order_items.extend(serializer.data)

        return Response(order_items, status=status.HTTP_200_OK)



































# ------------------------HOTEL ------------GET ORDER ITEMS



#----------------GET ALL ORDERED ITEMS ----------------------

class GetHotelOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)










#----------------GET ALL ORDERED ITEMS ROOMS----------------------

class GetHotelRoomsOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelRoomsOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelRoomsOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


























# ------------------------Restaurant ------------GET ORDER ITEMS



#----------------GET ALL ORDERED ITEMS ----------------------

class GetRestaurantOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RestaurantOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RestaurantOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


















# ------------------------Retails ------------GET ORDER ITEMS



#----------------GET ALL ORDERED ITEMS ----------------------

class GetRetailsOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = RetailsOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = RetailsOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





















#-------------------CHANGE  ORDER STATUS----------------------






#----------------------HOTEL  CHANGE ORDER STATUS-------------------


class HotelOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = HotelOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)







class HotelOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = HotelOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


















#----------------------HOTEL ROOMS CHANGE ORDER STATUS-------------------


class HotelRoomsOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelRoomsOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = HotelRoomsOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class HotelRoomsOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = HotelRoomsOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = HotelRoomsOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

















#----------------------------RESTAURANT ORDER STATUS---------------------------


#----------------------RESTAURANT  CHANGE ORDER STATUS-------------------


class RestaurantOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RestaurantOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RestaurantOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RestaurantOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RestaurantOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



















#----------------------------Retails ORDER STATUS---------------------------


#----------------------Retails  CHANGE ORDER STATUS-------------------


class RetailsOrderChangeStatusToTrueView(APIView):
    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsOrder.objects.get(id=cart_id)

            # Change the order status to True
            order.order_status = True
            order.save()

            # Change the order status of all ordered items to True
            ordered_items = RetailsOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=True)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class RetailsOrderChangeStatusToFalseView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        cart_id = int(request.query_params.get('id'))  # Replace with the appropriate way to get cartId from the request

        try:
            order = RetailsOrder.objects.get(id=cart_id)

            # Change the order status to False
            order.order_status = False
            order.save()

            # Change the order status of all ordered items to False
            ordered_items = RetailsOrderItems.objects.filter(order=order)
            ordered_items.update(order_status=False)

            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


















#-------------------DELETE ORDERS  ITEMS--------------------------

# EG: http://127.0.0.1:8000/Cart/HotelDeleteOrderItem/?cartId=14





#----------------DELETE HOTEL  ORDERED ITEMS---------------------
class HotelDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = HotelOrderItems.objects.get(id=cartId)
            plus_order = HotelOrderItems.objects.get(id=cartId)
            change_table = HotelOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            #NI KWA AJILI YA KUCHANGE TABLE STATUS
            OrderId = int(request.query_params.get('id'))
            items_count= HotelOrderItems.objects.filter(
                order__id__icontains = OrderId
                ).count()
            print(f"ORDER COUNT {items_count}")

            if items_count == 1:      
                #Change Table Status
                change_table.table.TableStatus = False
                change_table.table.save()

            #MWISHO NI KWA AJILI YA KUCHANGE TABLE STATUS


            order_item.delete()
 
            


            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except HotelOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



















#----------------DELETE HOTEL ROOMS ORDERED ITEMS---------------------
class HotelRoomsDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = HotelRoomsOrderItems.objects.get(id=cartId)
            plus_order = HotelRoomsOrderItems.objects.get(id=cartId)
            change_table = HotelRoomsOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            #NI KWA AJILI YA KUCHANGE TABLE STATUS
            OrderId = int(request.query_params.get('id'))
            items_count= HotelRoomsOrderItems.objects.filter(
                order__id__icontains = OrderId
                ).count()
            print(f"ORDER COUNT {items_count}")

            if items_count == 1:      
                #Change Table Status
                change_table.table.TableStatus = False
                change_table.table.save()

            #MWISHO NI KWA AJILI YA KUCHANGE TABLE STATUS


            order_item.delete()
 
            


            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



















#----------------DELETE Restaurant  ORDERED ITEMS---------------------
class RestaurantDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RestaurantOrderItems.objects.get(id=cartId)
            plus_order = RestaurantOrderItems.objects.get(id=cartId)
            change_table = RestaurantOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            #NI KWA AJILI YA KUCHANGE TABLE STATUS
            OrderId = int(request.query_params.get('id'))
            items_count= RestaurantOrderItems.objects.filter(
                order__id__icontains = OrderId
                ).count()
            print(f"ORDER COUNT {items_count}")

            if items_count == 1:      
                #Change Table Status
                change_table.table.TableStatus = False
                change_table.table.save()

            #MWISHO NI KWA AJILI YA KUCHANGE TABLE STATUS


            order_item.delete()
 
            


            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






















#----------------DELETE Retails  ORDERED ITEMS---------------------
class RetailsDeleteOrderItemView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cartId = request.query_params.get("cartId")

        user = request.user

        try:
            order_item = RetailsOrderItems.objects.get(id=cartId)
            plus_order = RetailsOrderItems.objects.get(id=cartId)
            change_table = RetailsOrderItems.objects.get(id=cartId)

            # Increase the product quantity back to stock
            order_item.product.ProductQuantity += order_item.quantity

            order_item.product.save()
            
            
            
            #Reduce order total price
            plus_order.order.total_price -= order_item.price
            plus_order.order.save()

            #NI KWA AJILI YA KUCHANGE TABLE STATUS
            OrderId = int(request.query_params.get('id'))
            items_count= RetailsOrderItems.objects.filter(
                order__id__icontains = OrderId
                ).count()
            print(f"ORDER COUNT {items_count}")

            if items_count == 1:      
                #Change Table Status
                change_table.table.TableStatus = False
                change_table.table.save()

            #MWISHO NI KWA AJILI YA KUCHANGE TABLE STATUS


            order_item.delete()
 
            


            return Response({"success": "Item deleted successfully in your order"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsOrdertems.DoesNotExist:
            return Response({"error": "Product not found in the order"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






























#------------COUNT ORDERS-------------------------------------





#------------HOTEL COUNT ORDERS------------------------------


class CountHotelOrderView(APIView):
    def get(self, request):
        try:
            _pending_orders = HotelOrder.objects.filter(
                order_status=False,
                total_price__gt = 0,
                room_number = None
            ).count()

            _approved_orders = HotelOrder.objects.filter(
                order_status=True,
                total_price__gt = 0,
                room_number = None
            ).count()

            _pending_orders_serializer = HotelOrderSerializer(
                HotelOrder.objects.filter(
                    order_status=False,
                    total_price__gt = 0,
                    room_number = None
                    ), many=True
            )

            _approved_orders_serializer = HotelOrderSerializer(
                HotelOrder.objects.filter(
                    order_status=True,
                    total_price__gt = 0,
                    room_number = None
                    ), many=True
            )

            response_data = {
                '_pending_orders': _pending_orders,
                '_approved_orders': _approved_orders,
                '_pending_orders_data': _pending_orders_serializer.data,
                '_approved_orders_data': _approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except HotelOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except HotelOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CountHotelRoomsOrderView(APIView):
    def get(self, request):
        try:
            Rooms_pending_orders = HotelRoomsOrder.objects.filter(
                order_status=False,
                total_price__gt = 0
            ).count()

            Rooms_approved_orders = HotelRoomsOrder.objects.filter(
                order_status=True,
                total_price__gt = 0
            ).count()

            Rooms_pending_orders_serializer = HotelRoomsOrderSerializer(
                HotelRoomsOrder.objects.filter(order_status=False,total_price__gt = 0), many=True
            )

            Rooms_approved_orders_serializer = HotelRoomsOrderSerializer(
                HotelRoomsOrder.objects.filter(order_status=True,total_price__gt = 0), many=True
            )

            response_data = {
                'Rooms_pending_orders': Rooms_pending_orders,
                'Rooms_approved_orders': Rooms_approved_orders,
                'Rooms_pending_orders_data': Rooms_pending_orders_serializer.data,
                'Rooms_approved_orders_data': Rooms_approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except HotelRoomsOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except HotelRoomsOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
























#----------------------------RESTAURANT COUNT ORDERS-------------------

class CountRestaurantOrderView(APIView):
    def get(self, request):
        try:
            _pending_orders = RestaurantOrder.objects.filter(
                order_status=False,
                total_price__gt = 0
            ).count()

            _approved_orders = RestaurantOrder.objects.filter(
                order_status=True,
                total_price__gt = 0
            ).count()

            _pending_orders_serializer = RestaurantOrderSerializer(
                RestaurantOrder.objects.filter(order_status=False,total_price__gt = 0), many=True
            )

            _approved_orders_serializer = RestaurantOrderSerializer(
                RestaurantOrder.objects.filter(order_status=True,total_price__gt = 0), many=True
            )

            response_data = {
                '_pending_orders': _pending_orders,
                '_approved_orders': _approved_orders,
                '_pending_orders_data': _pending_orders_serializer.data,
                '_approved_orders_data': _approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except RestaurantOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except RestaurantOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)








#---------------------RETAILS COUNT ORDERS----------------------

class CountRetailsOrderView(APIView):
    def get(self, request):
        try:
            _pending_orders = RetailsOrder.objects.filter(
                order_status=False,
                total_price__gt = 0
            ).count()

            _approved_orders = RetailsOrder.objects.filter(
                order_status=True,
                total_price__gt = 0
            ).count()

            _pending_orders_serializer = RetailsOrderSerializer(
                RetailsOrder.objects.filter(order_status=False,total_price__gt = 0), many=True
            )

            _approved_orders_serializer = RetailsOrderSerializer(
                RetailsOrder.objects.filter(order_status=True,total_price__gt = 0), many=True
            )

            response_data = {
                '_pending_orders': _pending_orders,
                '_approved_orders': _approved_orders,
                '_pending_orders_data': _pending_orders_serializer.data,
                '_approved_orders_data': _approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except RetailsOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except RetailsOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)















#------------------VIEWS FOR CLOSING BILL---------------------


#----------------HOTEL CLOSING BILL-------------------

class HotelOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = HotelOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = HotelOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



   
class HotelRoomsOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = HotelRoomsOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the is_customer_opened_closed of all ordered items to False
            ordered_items = HotelRoomsOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.is_customer_opened_closed = True  
                item.save()  
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except HotelRoomsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












#----------------RESTAURANT CLOSING BILL-------------------

class RestaurantOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = RestaurantOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = RestaurantOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RestaurantOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#----------------RETAILS CLOSING BILL-------------------

class RetailsOrderCloseBillView(APIView):
    def post(self, request):
        order_id = int(request.query_params.get('id'))

        try:
            # Fetch the order
            order = RetailsOrder.objects.get(id=order_id)

            # Change the closed_order_state to True
            order.closed_order_state = True
            order.save()

            # Change the TableStatus of all ordered items to False
            ordered_items = RetailsOrderItems.objects.filter(order=order)
            for item in ordered_items:
                item.table.TableStatus = False  # Update TableStatus to False
                item.table.save()  # Save the table status change
                
            return Response({"success": "Order status updated"}, status=status.HTTP_204_NO_CONTENT)

        except RetailsOrder.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






















#----------------REPORTS FOR HOTEL GUEST---------------------------




#------------GET ALL HOTEL REPORTS

class HotelGuestOrderReportView(APIView):
    
    def get(self, request):
        #Eg: http://127.0.0.1:8000/Cart/HotelOrderReport/?id=1&page=1&page_size=1
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed
            
            userId = int(request.query_params.get('id'))
            CategoryId = int(request.query_params.get('CategoryId'))

            orders = HotelOrder.objects.filter(
                user__id=userId,
                CategoryId=CategoryId,
                room_number__isnull=False  # Filter for non-None room_number
            ).order_by('order_status')

            # Calculate the main total price for all orders
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            

            
            

            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
                'main_total_price':main_total_price,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)













#-------------FILTER REPORT FOR GUEST CUSTOMERS-------------------

class FilterHotelGuestOrderReportView(APIView):
    def get(self, request):
        startDate = request.query_params.get("startDate") #"2023-09-10"
        endDate =request.query_params.get("endDate") # "2023-09-30"

        userId = int(request.query_params.get('id'))
        CategoryId = int(request.query_params.get('CategoryId'))

        

        # Filter orders based on date range
        orders = HotelOrder.objects.filter(
            user__id__icontains = userId,
            CategoryId=CategoryId,
            room_number__isnull=False,
            created__gte=startDate, created__lte=endDate
        ).order_by('order_status')

        # Calculate the main total price for filtered orders
        main_total_price = orders.aggregate(Sum("total_price"))["total_price__sum"]

        serializer = HotelOrderSerializer(orders, many=True)

        # Include the main total price in the response
        response_data = {
            "orders": serializer.data,
            "main_total_price": main_total_price,
        }

        return Response(response_data, status=status.HTTP_200_OK)













#---------COUNT ORDERS FOR HOTEL GUEST------------------



class CountHotelGuestOrderView(APIView):
    def get(self, request):
        try:
            _pending_orders = HotelOrder.objects.filter(
                order_status=False,
                total_price__gt = 0,
                room_number__isnull=False
            ).count()

            _approved_orders = HotelOrder.objects.filter(
                order_status=True,
                total_price__gt = 0,
                room_number__isnull=False
            ).count()

            _pending_orders_serializer = HotelOrderSerializer(
                HotelOrder.objects.filter(
                    order_status=False,
                    total_price__gt = 0,
                    room_number__isnull=False
                    ), many=True
            )

            _approved_orders_serializer = HotelOrderSerializer(
                HotelOrder.objects.filter(
                    order_status=True,
                    total_price__gt = 0,
                    room_number__isnull=False
                    ), many=True
            )

            response_data = {
                '_pending_orders': _pending_orders,
                '_approved_orders': _approved_orders,
                '_pending_orders_data': _pending_orders_serializer.data,
                '_approved_orders_data': _approved_orders_serializer.data,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except HotelOrder.DoesNotExist:
            return Response(
                {"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            

            

        except HotelOrder.DoesNotExist:
            return Response({"error": "Fails To Count Orders"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)














#------------GET ALL ORDERED ITEMS FOR GUEST CUSTOMERS------------



class GetHotelGuestOrderItemsView(APIView):
    def get(self, request):
        try:
            
            # page = int(request.query_params.get('page', 1))
            # page_size = int(request.query_params.get('page_size', 5)) 
            OrderId = int(request.query_params.get('id'))
            
            queryset = HotelOrderItems.objects.filter(
                order__id__icontains = OrderId
                )

            # paginator = PageNumberPagination()
            # paginator.page_size = page_size
            # page_items = paginator.paginate_queryset(queryset, request)

            serializer = HotelOrderItemsSerializer(queryset, many=True)

            response_data = {
                'queryset': serializer.data,
                # 'total_pages': paginator.page.paginator.num_pages, 
                # 'current_page': page,  
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)












#-----------REPORT FOR A SPECIFIC USER FOR GUEST CUSTOMERS--------------

class HotelGuestOrdersForSpecificUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        #http://127.0.0.1:8000/Cart/HotelOrder/?pages=1&page_size=2
        user = request.user
        try:
            # Get the page number from the query parameters, default to 1
            page = int(request.query_params.get('page', 1))
            page_size = int(request.query_params.get('page_size', 5))  # Adjust page size as needed

            #orders = HotelOrder.objects.all().order_by('-id')
            orders = HotelOrder.objects.filter(
                user=user,
                room_number__isnull = False
                ).order_by('order_status')
            main_total_price = orders.aggregate(Sum('total_price'))['total_price__sum']

            # Use pagination to get the desired page
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page_items = paginator.paginate_queryset(orders, request)

            serializer = HotelOrderSerializer(page_items, many=True)

            response_data = {
                'orders': serializer.data,
                'total_pages': paginator.page.paginator.num_pages,  # Send total pages info
                'current_page': page,  # Send current page info
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "orders":[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
























#--------------------COUNT ORDER FOR A SPECIFIC UESR/WAITER------------

#-------------THIS IS FOR WALKING CUSTOMERS-----------------

#--------------------HOTEL COUNT WAITERS ORDER------------------
class CountHotelOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_hotel_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                _pending_orders = HotelOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0,
                    room_number = None
                    #room_number__isnull=False
                    ).count()

                _approved_orders = HotelOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0,
                    room_number = None
                    #room_number__isnull=False
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "_pending_orders": _pending_orders,
                    "_approved_orders": _approved_orders,
                })

            serializer = HotelOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









class CountHotelRoomsOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_hotel_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                Rooms_pending_orders = HotelRoomsOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0
                    #room_number__isnull=False
                    ).count()

                Rooms_approved_orders = HotelRoomsOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0
                    #room_number__isnull=False
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "Rooms_pending_orders": Rooms_pending_orders,
                    "Rooms_approved_orders": Rooms_approved_orders,
                })

            serializer = HotelRoomsOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


















#--------------COUNT RESTAURANT WAITER ORDERS-----------------

class CountRestaurantOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_restaurant_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                _pending_orders = RestaurantOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0
                    ).count()

                _approved_orders = RestaurantOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "_pending_orders": _pending_orders,
                    "_approved_orders": _approved_orders,
                })

            serializer = RestaurantOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





















#---------COUNT RETAILS COUNT WAITER ORDER---------------------

class CountRetailsOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_retails_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                _pending_orders = RetailsOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0
                    #room_number__isnull=False
                    ).count()

                _approved_orders = RetailsOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "_pending_orders": _pending_orders,
                    "_approved_orders": _approved_orders,
                })

            serializer = RetailsOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



















#------------COUNT WAITERS ORDERS FOR GUEST CUSTOMERS---------


class CountHotelGuestOrderForEachUserView(APIView):
    def get(self, request):
        try:
            users = MyUser.objects.filter(
                is_hotel_user=True, 
                is_admin=False
                )
            user_data = []

            for user in users:
                _pending_orders = HotelOrder.objects.filter(
                    user=user,
                    order_status=False,
                    total_price__gt = 0,
                    # room_number = None
                    room_number__isnull=False
                    ).count()

                _approved_orders = HotelOrder.objects.filter(
                    user=user,
                    order_status=True,
                    total_price__gt = 0,
                    #room_number = None
                    room_number__isnull=False
                    ).count()

                user_data.append({
                    "id": user.id,
                    "username": user.username,
                    "_pending_orders": _pending_orders,
                    "_approved_orders": _approved_orders,
                })

            serializer = HotelOrderCountSerializer(user_data, many=True)       
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e), "queryset": []}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





