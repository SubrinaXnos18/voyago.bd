from django.contrib import admin
from .models import User, TourPackage, Booking, Payment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'email', 'phone', 'address')


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('package_id', 'title', 'duration', 'price')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'package', 'travel_date', 'status')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'booking', 'amount', 'payment_method', 'payment_date')
