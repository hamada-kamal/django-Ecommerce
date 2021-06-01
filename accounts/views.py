from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm , PasswordChangeForm
from django.contrib.auth import login , authenticate
from .models import Profile
from .forms import UserForm , ProfileForm
from django.contrib.auth.decorators import login_required
from product.models import Order
# Create your views here.



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            user = authenticate(username=username,password=password)
            login(request, user)
            return redirect('/products')

    else:
        form = UserCreationForm()

    context = {'form' : form}
    return render(request , 'registration/signup.html' , context)


@login_required(login_url='/accounts/login/')
def profile(request , slug):

    profile = get_object_or_404(Profile , slug=slug)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}  
        cartItems = order['get_cart_items']
    context = {'profile' : profile,'cartItems': cartItems}
    return render(request , 'profile.html' , context)