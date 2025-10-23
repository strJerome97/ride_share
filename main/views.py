
from rest_framework import viewsets, filters, exceptions
from django.db.models import F, Func, Value, FloatField
from django.db.models.expressions import ExpressionWrapper
from django.db.models.functions import Radians, Sin, Cos, ACos
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Prefetch
from datetime import timedelta

from .models import User, Ride, RideEvent
from .serializers import UserSerializer, RideSerializer, RideEventSerializer
from .filters import RideFilter
from .pagination import DefaultPagination

def haversine_distance_expression(lat_field, lon_field, lat, lon):
    R = 6371
    return ExpressionWrapper(
        ACos(
            Sin(Radians(Value(lat))) * Sin(Radians(F(lat_field))) +
            Cos(Radians(Value(lat))) * Cos(Radians(F(lat_field))) *
            Cos(Radians(F(lon_field)) - Radians(Value(lon)))
        ) * Value(R),
        output_field=FloatField()
    )

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
    ordering = ['pickup_time']

    def get_queryset(self):
        now = timezone.now()
        last_24_hours = now - timedelta(hours=24)
        ride_events_within_24_hours = RideEvent.objects.filter(created_at__gte=last_24_hours)
        
        values = Ride.objects.select_related('id_rider', 'id_driver').prefetch_related(
            Prefetch("events", queryset=ride_events_within_24_hours, to_attr="todays_ride_events")
        )
        
        lat = self.request.query_params.get('latitude')
        lon = self.request.query_params.get('longitude')
        
        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
            except ValueError:
                raise exceptions.ValidationError("Invalid latitude or longitude format.")
            
            values = values.annotate(
                distance=haversine_distance_expression('pickup_latitude', 'pickup_longitude', lat, lon)
            )
            self.ordering_fields = list(self.ordering_fields) + ['distance']
            self.ordering = ['distance'] + self.ordering
            
        return values

class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    