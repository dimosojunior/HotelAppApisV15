from import_export import resources
from HotelApis.models import *


class HotelProductsResource(resources.ModelResource):
	class Meta:
		model = HotelProducts






class HotelRoomsResource(resources.ModelResource):
	class Meta:
		model = HotelRooms