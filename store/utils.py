# Helper function that takes care of all repeated code for store_view, cart_view, checkout_view
import json
from.models import *
def helper(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderitems = order.orderitem_set.all()
        # totalItem is passed to the context dictionary to update the cart icon
        totalItem = order.totalItem

    else:
        # if cookies are stored parse from JSON format to a python dictionary 
        try:
            cart = json.loads(request.COOKIES['cart'])
            print(cart)
        # Set cart to an empty dictionary if above code fails to execute properly
        except:
            cart = {}
          
        orderitems = []
        order = {'grandCost':0, 'totalItem':0, 'shipping':False}
        totalItem = order['totalItem']
        # Looping through items in the cart dictionary and summing the total quantity of items
        for key in cart:
            try:
                totalItem += cart[key]['quantity']
                product = Product.objects.get(id=key)
                total = (product.price * cart[key]['quantity'])
                order['grandCost']+= total
                order['totalItem'] += cart[key]['quantity']
            
                item = {
                    'product':{
                        'id':product.id, 'name':product.name, 'price':product.price, 'imageURL':product.imageURL
                     },'quantity': cart[key]['quantity'], 'total':total
                }
                orderitems.append(item)
                print(orderitems)
                if product.digital == False:
                    order['shipping'] = True
            except:
                pass
    dicts = {'totalItem':totalItem, 'orderitems':orderitems, 'order':order}
    return dicts