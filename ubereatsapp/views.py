from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ubereatsapp.forms import UserForm, RestaurantForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


# Create your views here.

def home(request):
    return redirect(restaurant_home)


@login_required(login_url='/restaurant/sign-in/')
def restaurant_home(request):
    return render(request=request, template_name='restaurant/home.html')


def restaurant_sign_up(request):
    user_form = UserForm()
    restaurant_form = RestaurantForm()

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST, request.FILES)
        if user_form.is_valid() and restaurant_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()
            login(request=request, user=authenticate(
                user_name=user_form.cleaned_data["username"],
                password=user_form.cleaned_data["password"],
            ))
            return redirect(restaurant_home)
    return render(request=request,template_name='restaurant/sign_up.html',context={
        'user_form': user_form,
        'restaurant_form': restaurant_form
    })
