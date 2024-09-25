# Initializes the form folder

from .bookingForm import BookingForm
from .BusStatusForm import BusStatusForm
from .forms import (UpdateAccountForm,
                    RegistrationForm, RequestResetForm,
                    ResetPasswordForm, LoginForm)
from .passengerForm import PassengerForm
from .posts import PostForm

# Exposes the forms to the all application
__all__ = ['BookingForm', 'BusStatusForm', 'UpdateAccountForm',
           'RegistrationForm', 'RequestResetForm', 'LoginForm',
           'ResetPasswordForm', 'PassengerForm', 'PostForm']