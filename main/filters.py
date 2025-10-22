import django_filters as filters
from .models import Ride

class RideFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    rider_email = filters.CharFilter(method='filter_rider_email')
    
    def filter_rider_email(self, queryset, name, value):
        return queryset.filter(id_rider__email__icontains=value)
    
    class Meta:
        model = Ride
        fields = ['status', 'rider_email']
        