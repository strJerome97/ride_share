from django.db import models

class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Ride(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('en-route', 'En Route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='requested', db_index=True)
    id_rider = models.ForeignKey(User, related_name='rider', on_delete=models.CASCADE, null=True, blank=True)
    id_driver = models.ForeignKey(User, related_name='driver', on_delete=models.CASCADE, null=True, blank=True)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()
    
    def __str__(self):
        return f"Ride {self.id_ride} by User {self.id_rider.id_user}"

    class Meta:
        indexes = [
            models.Index(fields=['pickup_time']),
        ]
    
class RideEvent(models.Model):
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(Ride, related_name='events', on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Event {self.id_ride_event} for Ride {self.id_ride.id_ride}"
    