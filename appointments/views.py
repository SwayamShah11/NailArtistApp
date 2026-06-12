from django.shortcuts import render, redirect
from .models import Appointment
from .forms import AppointmentForm
from customers.models import Customer
from django.contrib.auth.decorators import login_required


@login_required
def appointment_list(request):

    appointments = Appointment.objects.filter(
        user=request.user
    ).order_by(
        'appointment_date',
        'appointment_time'
    )

    return render(
        request,
        'appointments/appointment_list.html',
        {
            'appointments': appointments
        }
    )


@login_required
def appointment_create(request):

    form = AppointmentForm(
        request.POST or None
    )

    if form.is_valid():

        appointment = form.save(
            commit=False
        )

        appointment.user = request.user

        customer, created = Customer.objects.get_or_create(
            user=request.user
        )

        appointment.customer = customer

        appointment.save()

        return redirect(
            'appointment_list'
        )

    return render(
        request,
        'appointments/appointment_form.html',
        {
            'form': form
        }
    )
