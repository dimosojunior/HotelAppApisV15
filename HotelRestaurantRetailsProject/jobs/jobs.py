from django.conf import settings
from django.core.mail import send_mail
from HotelApis.models import *

def schedule_api():
    orders = HotelRoomsOrderItems.objects.filter(DaysNumber=1)

    for order in orders:
        # Send an email to the user
        email = order.Customer.CustomerEmail
        subject = "Easy-Fix"
        message = "Muda 16 wako wa kuendelea kukaa chumbani umekwisha, jiandae kwa ajili ya kutoka"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=True)

        # Change RoomStatus in HotelRooms model to False
        room = order.room
        room.RoomStatus = False
        room.ProductQuantity = 1
        room.save()

        print(f"Email: {recipient_list}")
        print("HELLO")



#schedule_api()
