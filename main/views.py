
from rest_framework import viewsets, filters
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Prefetch
from datetime import timedelta

from .models import User, Ride, RideEvent
from .serializers import UserSerializer, RideSerializer, RideEventSerializer
from .filters import RideFilter
from .pagination import DefaultPagination

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = DefaultPagination

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    filterset_class = RideFilter
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['pickup_time']

class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    def get_queryset(self):
        now = timezone.now()
        last_24_hours = now - timedelta(hours=24)
        
        ride_events_within_24_hours = RideEvent.objects.filter(created_at__gte=last_24_hours)
        
        # values = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related(
        #     Prefetch("events", queryset=ride_events_within_24_hours, to_attr="todays_ride_events")
        # )
        
        print(str(ride_events_within_24_hours.values()))
        return ride_events_within_24_hours