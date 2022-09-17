from django.urls import path
from .views import *
urlpatterns = [
    path('<uuid:pk>/', BookDetailView.as_view(), name ='book_detail'),
    path('', BookListView.as_view(), name ='book_list'),
    path('reviewcreate/<uuid:pk>/', reviewcreate , name='reviewcreate'),
    path('cart/', cart, name='cart'),
    path('updatecart/', updatecart, name='updatecart'),
    path('checkout/', checkout, name='checkout'),
    path('orderprocess/', orderprocess, name='orderprocess'),
    path('success/', success, name='success')
]