from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string

from .models import Location, Booking
from config import settings


# Create your views here.
def home(request):
    return render(request, "booking/home.html")


def location_list(request):
    loc_list = Location.objects.filter(is_active=True)
    return render(request, "booking/locations.html", context={"locations": loc_list})


@login_required
def location_detail(request, location_id):
    location = get_object_or_404(Location, pk=location_id)
    error = ''
    if request.method == "POST":
        try:
            token = get_random_string(length=16)
            booking = Booking.objects.create(
                user=request.user,
                location=location,
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date'),
                token=token
            )
            url = f"{request.scheme}://{request.get_host()}" \
                  f"{reverse('main:activation', args=[booking.pk, token])}"
            send_mail(
                subject="Підтвердження бронювання",
                message=f"{url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[request.user.email],
                fail_silently=False
            )

            return redirect('main:home')
        except ValidationError as exp:
            error = exp.message
    return render(request, "booking/location_detail.html", context={"location": location,
                                                                    "error": error})


def activation_view(request, booking_id, token):
    booking = get_object_or_404(Booking, pk=booking_id)
    if booking.token == token:
        booking.is_confirmed = True
        booking.save()
    return redirect("main:home")


@login_required
def profile_view(request):
    return render(request, "booking/profile.html", {"bookings": request.user.bookings.order_by("-created_at")})
