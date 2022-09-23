import json
from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from django.urls import reverse_lazy, reverse
from .forms import ReviewForm, OrderItemForm
from django.http.response import HttpResponseRedirect, HttpResponse
from django.http import JsonResponse
from .utils import cookieCart


def bookListView(request):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(owner=request.user,complete=False)
            total_items = order.get_total_item
        except:
            total_items = 0
    else:
        cookieData = cookieCart(request)
        total_items = cookieData['total_items']

    books = Book.objects.all()
    context = {'books': books, 'total_items': total_items}
    return render(request, 'books/book_list.html', context)


def bookDetailView(request, pk):
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(owner=request.user,complete=False)
            total_items = order.get_total_items
        except:
            total_items = 0
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        total_items = 0
        for i in cart:
            print('this is cart', cart[i])
            total_items += cart[i]['quantity']
    book = Book.objects.get(id=pk)
    context = {'book': book, 'total_items': total_items}
    return render(request, 'books/book_detail.html', context)


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
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(owner=request.user, complete=False)
        except:
            return HttpResponseRedirect(reverse_lazy("book_list"))
        orderItems = order.orderitem_set.all()
        cart_total = order.get_total_cart
        total_items = order.get_total_items
    else:
        cookieData = cookieCart(request)
        if cookieData.length > 0:
            orderItems = cookieData['orderItems']
            cart_total = cookieData['cart_total']
            total_items = cookieData['total_items']
        else:
            return HttpResponseRedirect(reverse_lazy("book_list"))


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
    if request.user.is_authenticated:
        try:
            order = Order.objects.get(owner=request.user, complete=False)
        except:
            return HttpResponseRedirect(reverse_lazy("book_list"))
        orderItems = order.orderitem_set.all()
        cart_total = order.get_total_cart
        total_items = order.get_total_items
    else:
        cookieData = cookieCart(request)
        if cookieData>0:
            orderItems = cookieData['orderItems']
            cart_total = cookieData['cart_total']
            total_items = cookieData['total_items']
        else:
            return HttpResponseRedirect(reverse_lazy("book_list"))
    context = {'items': orderItems, 'cart_total': cart_total, 'total_items': total_items}
    return render(request, 'cart/checkout.html', context)


def orderprocess(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        order = Order.objects.get(owner=request.user, complete=False)
    else:
        cookieData = cookieCart(request)
        orderItems = cookieData['orderItems']
        order = Order.objects.create()
        for item in orderItems:
            orderItem = OrderItem.objects.create(order=order,
                                                 book=item['book']['id'],
                                                 quantity=item['quantity'],
                                                 )
            orderItem.save()

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