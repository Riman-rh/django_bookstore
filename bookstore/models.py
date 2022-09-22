from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          editable=False)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    date_published = models.DateField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    cover = models.ImageField(upload_to='covers/')

    def __str__(self):
        return self.title

    @property
    def get_absolute_url(self):
        return reverse('book_detail', args=[str(self.id)])


class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=1,
                                         validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'review {self.review[:5]} by {self.owner}'


class Order(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
    complete = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_cart(self):
        orderItems = self.orderitem_set.all()
        total = 0
        for item in orderItems:
            total = total + item.quantity * item.book.price
        return total

    @property
    def get_total_items(self):
        orderItems = self.orderitem_set.all()
        total = 0
        for item in orderItems:
            total = total + item.quantity
        return total

    def __str__(self):
        return f'order n {self.id} by {self.owner}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def get_total_item(self):
        return self.book.price * self.quantity

    def __str__(self):
        return f'orderItem {self.book}'


class Shipping(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=225)
    zipcode = models.IntegerField(null=True)
    phone = models.CharField(max_length=200)

