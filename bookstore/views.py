import json
from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from django.urls import reverse_lazy, reverse
from .forms import ReviewForm, OrderItemForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth import get_user_model


class BookListView(ListView):
    model = Book
    context_object_name = 'books'
    template_name = 'books/book_list.html'


class BookDetailView(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'books/book_detail.html'


def reviewcreate(request, pk):
    form = ReviewForm(request.POST)
    book = Book.objects.get(id=pk)
    if form.is_valid():
        review = form.save(commit=False)
        review.owner = request.user
        review.book = book
        review.save()
        return HttpResponseRedirect(reverse_lazy('book_list'))
    return HttpResponse(form.errors)


def orderprocess(request):
    order, created = Order.objects.get_or_create(owner=request.user, complete=True)
    for item in request.POST:
        form = OrderItemForm(item)
        if form.is_valid():
            item = form.save(commit=False)
            item.order = order
            item.save()
        return HttpResponse("something wrong occure!")


def cart(request):
    try:
        order = Order.objects.get(owner=request.user, complete=False)
    except:
        return HttpResponseRedirect(reverse_lazy("book_list"))
    orderItems = order.orderitem_set.all()
    cart_total = order.get_total_cart
    total_items = order.get_total_items
    context = {'items': orderItems, 'cart_total': cart_total, 'total_items': total_items}
    return render(request, 'cart/cart.html', context)


def updatecart(request):
    data = json.loads(request.body)
    bookId = data['bookId']
    action = data['action']
    book = Book.objects.get(id=bookId)
    order, created = Order.objects.get_or_create(owner=request.user, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, book=book)
    if action == 'add':
        orderItem.quantity = orderItem.quantity+1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity -1

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('update cart ', safe=False)


def checkout(request):
    order = Order.objects.get(owner=request.user, complete=False)
    orderItems = order.orderitem_set.all()
    cart_total = order.get_total_cart
    total_items = order.get_total_items
    user = get_user_model().objects.get(username=request.user.username)
    context = {'items': orderItems, 'cart_total': cart_total, 'total_items': total_items, 'order':order}
    return render(request, 'cart/checkout.html', context)


def orderprocess(request):
    data = json.loads(request.body)
    order = Order.objects.get(owner=request.user, complete=False)
    shipping, created = Shipping.objects.get_or_create(order=order)
    shipping.lastname = data['formData']['lastname']
    shipping.firstname = data['formData']['firstname']
    shipping.email = data['formData']['email']
    shipping.address = data['formData']['address']
    shipping.zipcode = int(data['formData']['zipcode'])
    shipping.phone = data['formData']['phone']
    shipping.save()
    order.complete = True
    order.save()
    return HttpResponse("data added", safe=False)


def success(request):
    return render(request, 'cart/success.html')