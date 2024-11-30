from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return self.name


class TourPackage(models.Model):
    package_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField()  # Duration in days
    price = models.FloatField()
    available_dates = models.JSONField()  # List of available dates (can use JSONField)

    def __str__(self):
        return self.title


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField(auto_now_add=True)
    travel_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending')

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user}"


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    amount = models.FloatField()
    payment_method = models.CharField(max_length=50)
    payment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} for Booking {self.booking.booking_id}"


