from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User as AuthUser
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, TourPackage, Booking, Payment
from django.contrib.auth.decorators import login_required

# User Registration
def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if not AuthUser.objects.filter(username=username).exists():
                auth_user = AuthUser.objects.create_user(username=username, email=email, password=password)
                auth_user.save()
                User.objects.create(name=username, email=email)
                messages.success(request, 'Registration successful! Please login.')
                return redirect('login')
            else:
                messages.error(request, 'Username already exists.')
        else:
            messages.error(request, 'Passwords do not match.')

    return render(request, 'register.html')


# User Login
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('view_packages')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')


# User Logout
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def view_packages(request):
    packages = TourPackage.objects.all()
    user_bookings = Booking.objects.filter(user__name=request.user.username)
    return render(request, 'packages.html', {'packages': packages, 'bookings': user_bookings})


# Book a Package
def book_package(request, package_id):
    package = TourPackage.objects.get(package_id=package_id)
    print(f"Package selected: {package.title}")  # Debug print
    if request.method == 'POST':
        travel_date = request.POST['travel_date']
        user = User.objects.get(name=request.user.username)  # Make sure the user is authenticated
        booking = Booking.objects.create(user=user, package=package, travel_date=travel_date, status="Pending")
        print(f"Booking created with ID: {booking.booking_id}")  # Debug print
        return redirect('process_payment', booking_id=booking.booking_id)
    return render(request, 'book_package.html', {'package': package})



# Process Payment
def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    if request.method == 'POST':
        payment_method = request.POST['payment_method']
        amount = booking.package.price

        # Create the payment without using a local variable
        Payment.objects.create(
            booking=booking,
            amount=amount,
            payment_method=payment_method,
            payment_date=request.POST.get('payment_date'),
        )

        # Update booking status after payment
        booking.status = 'Confirmed'
        booking.save()

        return redirect('view_packages')  # Redirect to packages page after payment is done

    return render(request, 'payment.html', {'booking': booking})


@login_required
def user_profile(request):
    user = User.objects.get(name=request.user.username)
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']

        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')

    return render(request, 'profile.html', {'user': user})

# Payment Success Page
@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id)
    return render(request, 'payment_success.html', {'booking': booking})

# Cancel Booking
@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, booking_id=booking_id, user__name=request.user.username)
    if booking.status == 'Confirmed':
        booking.status = 'Refunded'
        booking.save()

        # Update payment status (optional, if required for admin visibility)
        Payment.objects.filter(booking=booking).update(amount=0)
        messages.success(request, 'Booking canceled and refunded successfully!')
    else:
        messages.error(request, 'Booking cannot be canceled.')
    return redirect('view_packages')

