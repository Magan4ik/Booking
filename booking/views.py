from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from .models import Location, Booking


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
            booking = Booking.objects.create(
                user=request.user,
                location=location,
                start_date=request.POST.get('start_date'),
                end_date=request.POST.get('end_date')
            )
            return redirect('main:home')
        except ValidationError as exp:
            error = exp.message
    return render(request, "booking/location_detail.html", context={"location": location,
                                                                    "error": error})
