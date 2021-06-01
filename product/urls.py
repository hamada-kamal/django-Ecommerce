from django.urls import path
from . import views


app_name = 'product'

urlpatterns = [
    
    path('',views.all_product , name='store'),
    path('autosearch',views.autoSearch , name='autosearch'),
    path( '<slug:slug>', views.product_detail , name='product_detail'),
    path('cart/',views.cart , name='cart'),
    path('checkout/',views.checkout , name='checkout'),
    path('update_item/', views.updateItem, name="update_item"),
    path('like_item/', views.likeItem, name="like_item"),
    path('favorites/', views.liked_product, name="liked_product"),
    path('process_order/', views.processOrder, name="process_order"),
    
    
] 
