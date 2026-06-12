from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileForm, UserUpdateForm
from .models import CustomerProfile


def register_view(request):

    form = RegisterForm(
        request.POST or None
    )

    if form.is_valid():

        user = form.save()

        login(
            request,
            user
        )

        return redirect(
            'home'
        )

    return render(
        request,
        'accounts/register.html',
        {
            'form': form
        }
    )


def logout_view(request):

    logout(request)

    return redirect(
        'home'
    )


@login_required
def profile_view(request):

    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        user_form = UserUpdateForm(
            request.POST,
            instance=request.user
        )

        profile_form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if (
            user_form.is_valid()
            and profile_form.is_valid()
        ):

            user_form.save()
            profile_form.save()

            return redirect('profile')

    else:

        user_form = UserUpdateForm(
            instance=request.user
        )

        profile_form = ProfileForm(
            instance=profile
        )

    return render(
        request,
        'accounts/profile.html',
        {
            'user_form': user_form,
            'profile_form': profile_form,
            'profile': profile
        }
    )
