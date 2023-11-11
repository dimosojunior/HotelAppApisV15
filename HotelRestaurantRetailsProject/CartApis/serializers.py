from rest_framework import serializers

class HotelOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    _pending_orders = serializers.IntegerField()
    _approved_orders = serializers.IntegerField()




class HotelRoomsOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    Rooms_pending_orders = serializers.IntegerField()
    Rooms_approved_orders = serializers.IntegerField()









class RestaurantOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    _pending_orders = serializers.IntegerField()
    _approved_orders = serializers.IntegerField()












class RetailsOrderCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    _pending_orders = serializers.IntegerField()
    _approved_orders = serializers.IntegerField()



