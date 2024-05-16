from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views import View

from .forms import UserLoginForm
from .forms import ProfileForm
from .forms import RegistrationForm
from .forms import ChangePasswordForm
from django.contrib.auth import update_session_auth_hash
from .models import PurchaseHistory, Address


def index(request):
    return render(request, 'users/index.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products:parent_categories')
    else:
        form = RegistrationForm()
    return render(request, 'products/index.html', {'form': form})


def user_login(request):
    form = UserLoginForm(data=request.POST)

    if form.is_valid():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print(user)
            return redirect('products:parent_categories')
    else:
        form = UserLoginForm()
    return render(request, 'products/base.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('products:parent_categories')


class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('user:login')

        user = request.user
        addresses = Address.objects.all()
        purchase_history = PurchaseHistory.objects.filter(user=user)

        context = {'user': user, 'addresses': addresses, 'purchase_history': purchase_history}
        return render(request, 'users/profile.html', context)

    def put(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Пользователь не аутентифицирован.'}, status=401)

        user = request.body
        form = ProfileForm(request.PUT, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
        else:
            # Handle invalid form
            pass


@login_required
def profile_field(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Пользователь не аутентифицирован.'}, status=401)

    user_profile = request.user
    try:
        addresses_query = user_profile.address_set.all().values('address_line1', 'city', 'country')
        addresses = [", ".join([str(value) for value in address_data.values()]) for address_data in addresses_query]

        user_data = {
            'username': user_profile.username,
            'email': user_profile.email,
            'first_name': user_profile.first_name,
            'last_name': user_profile.last_name,
            'phone_number': user_profile.phone_number,
            'addresses': addresses,
        }

        return JsonResponse(user_data, safe=False)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Продукт с указанным идентификатором не найден.'}, status=404)



def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Важно, чтобы пользователь оставался аутентифицированным после смены пароля
            return redirect('profile')  # Перенаправляем пользователя на страницу профиля после успешного изменения пароля
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'account/change_password.html', {'form': form})

