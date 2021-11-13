from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.

class Customer(models.Model):
    # Associating a Cutomer with the custom  django user model. 
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    # It can also be done this way user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False )
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return self.name
        
    @property
    def imageURL(self):
        try:
            url = self.image.url
            
        except:
            url = ""
        return url

class Order(models.Model):
    # Associating every order with a customer
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True) 
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return 'Order '+str(self.id)
    
    # This shipping method checks all the orderitems and decides if shipping is required
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for item in orderitems:
            if item.product.digital == False:
                shipping = True
        return shipping

    
    @property
    def grandCost(self):
        # Querying to get all orderitems for an order
        totalItems = self.orderitem_set.all()
        # for all the orderitems we call the total method for Orderitem and get the sum  
        total = sum([item.total for item in totalItems])
        return total

    @property
    def totalItem(self):
        totalItems = self.orderitem_set.all()
        # for all the orderitems on each order we call quantity attribute and get the sum
        total = sum([item.quantity for item in totalItems])
        return total

class OrderItem(models.Model):
    # Associating every orderitem with a product
    product = models.ForeignKey(Product,on_delete=models.SET_NULL, null=True)
    # Associating every orderitem with an order or cart in this case
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
     
    @property
    def total(self):
        total = self.quantity * self.product.price
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address) # because we are using dunder method string