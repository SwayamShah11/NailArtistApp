from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):

    class Meta:

        model = Appointment

        fields = (
            'service',
            'appointment_date',
            'appointment_time',
            'notes'
        )

        widgets = {
            'appointment_date':
                forms.DateInput(
                    attrs={'type': 'date'}
                ),

            'appointment_time':
                forms.TimeInput(
                    attrs={'type': 'time'}
                )
        }
