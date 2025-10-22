from rest_framework import serializers
from .models import User, Ride, RideEvent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'
        
class RideEventSerializer(serializers.ModelSerializer):
    # todays_ride_events = serializers.SerializerMethodField()
    
    class Meta:
        model = RideEvent
        fields = [
            "id_ride_event",
            "id_ride",
            "description",
            "created_at",
            # "todays_ride_events"
            ]
        
    # def get_todays_ride_events(self, obj):
    #     events = getattr(obj, 'todays_ride_events', [])
    #     return RideEventSerializer(events, many=True).data

