
from django.urls import path
from travel import views  # Replace 'travel' with your app name

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('packages/', views.view_packages, name='view_packages'),
    path('book/<int:package_id>/', views.book_package, name='book_package'),
    path('payment/<int:booking_id>/', views.process_payment, name='process_payment'),
    path('profile/', views.user_profile, name='user_profile'),
    path('payment/success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    # Root path: Redirect to view_packages
    path('', views.view_packages, name='home'),


]
