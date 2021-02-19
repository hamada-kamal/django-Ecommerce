from django.shortcuts import render , get_object_or_404, redirect, reverse
from .models import Customer, Product, Order, OrderItem, ShippingAddress
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import datetime

# def userlogged(request):
#     customer = request.user.customer
#     return render(request, 'base.html', {'customer':customer})


def all_product(request):
    search_qs = request.GET.get('searchname', '')
    if search_qs:
        products = Product.objects.filter(name__icontains=search_qs)
    else:
        products = Product.objects.all()

    paginator = Paginator(products, 3) 
    pages = request.GET.get('page')
    products = paginator.get_page(pages)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems = order['get_cart_items']

  

    context = {'products' : products, 'cartItems': cartItems,}
    return render(request , 'product/store.html' , context)



def product_detail(request , slug):
    product = get_object_or_404(Product ,PRDSLug=slug )
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}  
        cartItems = order['get_cart_items']
    context = {'product' : product, 'cartItems': cartItems,}
    return render(request , 'product/detail.html' , context)




def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        items = []
        cartItems = order['get_cart_items']
    return render(request, 'product/cart.html', {'items':items, 'order': order, 'cartItems': cartItems})

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        items = []
        cartItems = order['get_cart_items']
    return render(request, 'product/checkout.html', {'items':items, 'order': order, 'cartItems': cartItems})


def updateItem(request):
    datat = json.loads(request.body)

    productId=datat['productId']
    action =datat['action']
    print('action',action)
    print('productId',productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        if orderItem.quantity>1:
            orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0     
    orderItem.save()
    if  orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)     


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
        	order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )

    else:
        print("user not loged in ..")

    return JsonResponse('payment complete', safe=False)   

def likeItem(request):
    datat = json.loads(request.body)

    productId=datat['productId']
    action =datat['action']
    # print('action',action)
    # print('productId',productId)
    if action == 'add':
        customer = request.user.customer
        product = Product.objects.get(id=productId)
        if customer in product.like.all():
            product.like.remove(customer)
        else:
            product.like.add(customer)

    return JsonResponse('Item was liked or unliked', safe=False) 



def liked_product(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        products = Product.objects.filter(like=customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems = order['get_cart_items']
    return render(request, 'product/favorit.html', {'products':products, 'cartItems': cartItems})


def autoSearch(request):
    print(request.GET)
    q_original = request.GET.get('term')
    qs = Product.objects.filter(name__icontains = q_original)
    if qs:
        print('this is',qs)
        names = []
        names+=[x.name for x in qs]
    else:
        names = ['No results']
    return JsonResponse(names, safe=False)
    