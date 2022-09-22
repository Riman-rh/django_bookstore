import json
from .models import *
def cookieCart(request):
     try:
        cart = json.loads(request.COOKIES['cart'])
        print('Cart', cart)
     except:
        cart = {}
     orderItems = []
     total_items = 0
     cart_total = 0
     for i in cart:
        total_items += cart[i]['quantity']
        try:
            book = Book.objects.get(id=i)
            total = book.price * cart[i]['quantity']
            cart_total += total
            item = {
                'book':{
                    'id': book.id,
                    'title': book.title,
                    'price': book.price,
                    'cover': book.cover
                },
                'quantity': cart[i]['quantity'],
                'get_total_item': total
            }
            orderItems.append(item)
        except:
            pass

     return {'orderItems':orderItems, 'total_items': total_items, 'cart_total':cart_total}