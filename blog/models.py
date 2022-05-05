from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-id"]


class Item(models.Model):
    name = models.CharField(max_length=1000)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}, {self.price} KZT"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def total(self):
        cart_items = CartItem.objects.filter(cart=self)
        s = 0
        for cart_item in cart_items:
            s = s + cart_item.item.price * cart_item.count

        return s

    def __str__(self):
        return f"Cart of {self.user.username}, total: {self.total()} KZT"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.item}, {self.count} pc"
