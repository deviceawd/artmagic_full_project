from django.urls import path
from . import views


app_name = 'products'

urlpatterns = [
    path('', views.parent_categories, name='parent_categories'),
    path('category/<str:slug>/', views.sub_categories, name='sub_categories'),
    path('product/<str:slug>/', views.sub_product, name='sub_product'),
    path('products/', views.products_view, name='products_list'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('detail/<str:slug>/', views.detail, name='product_detail'),
]