from django.urls import path
from app import views
from app.views import *
from django.contrib.auth import views as auth_view
from app.forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django_ratelimit.decorators import ratelimit


urlpatterns = [
    path('', ProductView.as_view(), name='home'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),

    path('update_cart/<int:cart_id>/', views.update_cart, name='update_cart'),

    path('cart/', views.show_cart, name='cart'),

    # path('pluscart/', views.plus_cart, name='plus_cart'),

    path('buy/', views.buy_now, name='buy-now'),

    path('profile/', views.ProfileView.as_view(), name='profile'),

    path('checkout/', views.checkout, name='checkout'),

    path('paymentdone/', views.payment_done, name='paymentdone'),

    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),

    # path('password-reset/', views.change_password, name='password_reset'),

    path('mobile/', views.MobileView.as_view(), name='mobile'),
    path('mobile/<slug:data>/', views.MobileView.as_view(), name='mobiledata'),

    path('laptop/', views.LaptopView.as_view(), name='laptop'),
    path('laptop/<slug:data>/', views.LaptopView.as_view(), name='laptopdata'),

    path('topwear/', views.TopwearView.as_view(), name='topwear'),
    path('topwear/<slug:data>/', views.TopwearView.as_view(), name='topweardata'),

    path('bottomwear/', views.BottomwearView.as_view(), name='bottomwear'),
    path('bottomwear/<slug:data>/', views.BottomwearView.as_view(), name='bottomweardata'),


    #set rate rate limiter
    path('accounts/login/', ratelimit(key='post:username', rate='5/m')(auth_view.LoginView.as_view(template_name='app/login.html', success_url='home', authentication_form=LoginForm)), name='login'),

    path('logout/', ratelimit(key='get:username', rate='5/m')(auth_view.LogoutView.as_view(next_page='login')), name='logout'),

    path('passwordchange/', ratelimit(key='post:username', rate='5/m')(auth_view.PasswordChangeView.as_view(template_name='app/passwordchange.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone/')), name='passwordchange'),

    path('passwordchangedone/', ratelimit(key='post:username', rate='5/m')(auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html')), name='passwordchangedone'),

    path('password-reset/', ratelimit(key='post:username', rate='5/m')(auth_view.PasswordResetView.as_view(template_name='app/password_reset.html', form_class=MyPasswordResetForm)), name='password_reset'),

    path('password-reset/done/', ratelimit(key='post:username', rate='5/m')(auth_view.PasswordChangeDoneView.as_view(template_name='app/password_reset_done.html')), name='password_reset_done'),

    path('password-reset-complete/', ratelimit(key='post:username', rate='5/m')(auth_view.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html')), name='password_reset_complete'),

    path('password-reset-confirm/<uidb64>/<token>/', ratelimit(key='post:username', rate='5/m')(auth_view.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html', form_class=MySetPasswordForm)), name='password_reset_confirm'),

    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),

    path('search/', views.search, name='search'),
    path('remove/<int:id>/', views.remove_item, name='remove'),
    path('comment/', views.CommentView.as_view(), name='comment'),
    path('about/', views.about, name='about'),
    path('add-product/', ProductAddView.as_view(), name='add_product'),
    path('update-product/<int:pk>/', updateProduct, name='update_product'),
    path('delete-product/<int:pk>/', deleteProduct, name='delete_product'),
]
