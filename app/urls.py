from app.views.auth import my_account, login_view, logout_view, register_page
from app.views.cart import product_cart_page, add_cart_view, delete_cart_view, edit_cart_item_view
from app.views.checkout import checkout_view
from app.views.other import product_details_view, shop_view, add_product_view, edit_product, delete_product, \
    product_error404, product_compare_page, product_checkout_page, product_blog, product_blog_details_page, about_page, \
    contact_page, index_view, product_frequently_questions
from app.views.wishlist import product_wishlist_page, delete_wishlist_view, add_wishlist_view
from django.urls import path

urlpatterns = [
    path('', index_view, name='index'),
    path('shop-main-page/', shop_view, name='shop_main'),
    path('<int:product_id>/', product_details_view, name='product-details'),
    path('add-product/', add_product_view, name='add-product'),
    path('edit-product/<int:product_id>', edit_product, name='edit-product'),
    path('delete-product/<int:product_id>', delete_product, name='delete-product'),

    path('product-wishlist-page/', product_wishlist_page, name='product-wishlist-page'),
    path('add-wishlist/<int:product_id>', add_wishlist_view, name='add-wishlist'),
    path('delete-wishlist/<int:product_id>', delete_wishlist_view, name='delete-wishlist'),

    path('product-cart-page/', product_cart_page, name='product-cart-page'),
    path('add-cart/<int:product_id>', add_cart_view, name='add-cart'),
    path('delete-cart/<int:product_id>', delete_cart_view, name='delete-cart'),
    path('edit-cart/<int:product_id>', edit_cart_item_view, name='edit-cart '),

    path('product-checkout-page/', checkout_view, name='product-checkout-page'),

    path('product-error404-page/', product_error404, name='product-error404'),
    path('product-compare-page/', product_compare_page, name='product-compare-page'),
    path('product-checkout-page/', product_checkout_page, name='product-checkout-page'),
    path('product-frequently-questions-page/', product_frequently_questions, name='product-frequently-questions-page'),
    path('product-blog_main-page/', product_blog, name='product-blog-page'),
    path('product-blog_details-page/<int:blog_id>/', product_blog_details_page, name='product-blog-details-page'),
    path('about-page/', about_page, name='about'),
    path('contact-page/', contact_page, name='contact'),

    path('my-account-page/', my_account, name='my-account'),
    path('login-page/', login_view, name='login'),
    path('logout-page/', logout_view, name='logout'),
    path('register-page/', register_page, name='register')


]
