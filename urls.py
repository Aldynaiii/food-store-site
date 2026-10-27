from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),               
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_order/', views.create_order, name='create_order'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('', views.index, name='index'),
    path('reviews/', views.leave_feedback,{'order_id': 1}, name='reviews'),
    path('product/<int:product_id>/', views.product_detail,name='product_detail'),
    path('profile/', views.profile_view, name='profile'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
]

