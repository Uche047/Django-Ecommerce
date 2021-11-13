from django.shortcuts import render
from.models import *
from django.http import JsonResponse
from.utils import helper # Importing helper function that does all neccesary calculations
import json
import datetime
# Create your views here.
    
def store_view(request):
    products = Product.objects.all()
    dicts = helper(request)
    totalItem = dicts['totalItem']

    context = {'products':products,'totalItem':totalItem}
    return render(request, "store/store.html",context)

def cart_view(request):
    dicts = helper(request)
    totalItem = dicts['totalItem']
    order = dicts['order']
    orderitems = dicts['orderitems']
   
    context = {'orderitems':orderitems, 'order':order, 'totalItem':totalItem}
    return render(request, "store/cart.html",context)

def checkout_view(request):
    dicts = helper(request)
    totalItem = dicts['totalItem']
    order = dicts['order']
    orderitems = dicts['orderitems']

    context = {
        'orderitems':orderitems, 'order':order, 'totalItem':totalItem, 'shipping':False
    }
    return render(request, "store/checkout.html",context)

def updateItem_view(request):
    # request.body contains data we sent in JSON format
    # json.loads converts it into a dictionary like format or an object in javascript
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    # Getting an order or creating one where it does not exist
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    # Getting an order or creating one where it does not exist
    orderItem,created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("Item was just added", safe=False)

def processOrder_view(request):
    #Creating a transaction id using the python datetime module and object
    transaction_id = datetime.datetime.now().timestamp()
    # Converting json to python format or dictionary object
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        # Getting the total cost from the checkout.html frontend side
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        # comparing the total cost from what was sent to the backend using the fetch api to compare
        # results computed in the backend
        if total == float(order.grandCost):
            order.complete = True
        order.save()

        if order.shipping == True:
            #Creating a new shipping object if there is a non-digital object
            ShippingAddress.objects.create(
                customer=customer,order=order,address=data['shipping']['address'],city=data['shipping']['city'], state=data['shipping']['state'],zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User not logged in')
        print('COOKIES', request.COOKIES)
        name = data['form']['name']
        email = data['form']['email']
        dicts = helper(request)
        orderitems = dicts['orderitems']
        # Creating a customer who can shop as many times as the guest user recognized by the guest's email 
        # Shops on the site without creating a new customer with every visit to the site
        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()
     
    return JsonResponse('Payment Complete', safe=False)