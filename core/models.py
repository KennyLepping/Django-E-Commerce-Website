from django.conf import settings
from django.db import models
from django.shortcuts import reverse

CATEGORY_CHOICES = (
    ('S','Shirt'), # First parameter is what goes in the DB and 2nd is what's displayed
    ('SW','Sportwear'),
    ('OW','Outwear')
)

LABEL_CHOICES = (
    ('P','primary'), # First parameter is what goes in the DB and 2nd is what's displayed
    ('S','secondary'), # primary, secondary... are from the Bootstrap CSS colors
    ('D','danger')
)

# An Item becomes an OrderItem when in the shopping cart 
class Item(models.Model): # Way of linking between the order and the item itself
    title = models.CharField(max_length=100)
    price = models.FloatField()

    # blank and null are true so we don't have to have a discount price
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = models.TextField()    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })
    
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        }) 


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class Order(models.Model): # Is like the shopping cart, all order items go in here
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
