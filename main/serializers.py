from rest_framework import serializers
from .models import User, Ride, RideEvent

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class RideSerializer(serializers.ModelSerializer):
    rider = UserSerializer(source='id_rider', read_only=True)
    driver = UserSerializer(source='id_driver', read_only=True)
    distance = serializers.FloatField(read_only=True)
    todays_ride_events = serializers.SerializerMethodField()
    
    class Meta:
        model = Ride
        fields = '__all__'
        
    def get_todays_ride_events(self, obj):
        events = getattr(obj, 'todays_ride_events', [])
        return RideEventSerializer(events, many=True).data
        
class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvent
        fields = [
            "id_ride_event",
            "id_ride",
            "description",
            "created_at",
        ]

