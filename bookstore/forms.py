from .models import Review, OrderItem
from django import forms
from django.contrib.auth import get_user_model

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["rating", "review"]


class OrderItemForm(forms.ModelForm):

    class Meta:
        model = OrderItem
        fields = ['book', 'quantity']

