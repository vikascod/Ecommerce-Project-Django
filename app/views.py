from django.shortcuts import render, redirect
from app.models import Product, Cart, Customer, OrderPlaced, Comment
from django.views.generic import View
from app.forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm, CommentForm, ProductForm, UpdateProductForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from django.contrib.auth.mixins import UserPassesTestMixin


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)



class ProductAddView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            total_item = 0
            form = ProductForm()
            if request.user.is_authenticated:
                total_item = len(Cart.objects.filter(user=request.user))
            context = {
                'form':form,
                'total_item':total_item
            }
            return render(request, 'app/addproduct.html', context)
        else:
            return HttpResponse("No Permission!")


    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                user = request.user
                new_product = form.save(commit=False)
                new_product.user = user
                new_product.save()
                messages.success(request, "Product Successfully Added!")
                return redirect('home')
            
            context = {
                'form':form,
                }
            return render(request, 'app/addproduct.html', context)
        else:
            return HttpResponse("No Permission!")



@login_required(login_url='login')
def deleteProduct(request, pk):
    if request.user.is_staff:
        product = Product.objects.get(pk=pk)
        if cache.get(pk) == product:
            product.delete()
        else:
            cache.delete(pk)
            product.delete()
        messages.success(request, "Successfully product deleted!")
        return redirect('home')
    else:
        return HttpResponse("You don't have permission!")




@login_required(login_url='login')
def updateProduct(request, pk):
    if request.user.is_staff:
        product = Product.objects.get(pk=pk)
        form = UpdateProductForm(instance=product)
        if request.method == 'POST':
            form = UpdateProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, "Product Successfully Updated!")
                return redirect('home')
        context = {'form':form}
        return render(request, 'app/updateproduct.html', context)
    else:
        return HttpResponse("You don't have permission!")




class ProductView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        total_item = 0

        bottomwears = cache.get('all_bottomwears')
        if bottomwears is None:
            bottomwears = Product.objects.filter(category='BW')
            cache.set('all_bottomwears', bottomwears, CACHE_TTL)
            print(print("Hit bottomwears db"))
        else:
            print("Hit bottomwears cache")

        topwears = cache.get('all_topwears')
        if topwears is None:
            topwears = Product.objects.filter(category='TW')
            cache.set('all_topwears', topwears, CACHE_TTL)
            print("Hit topwears db")
        else:
            print("Hit topwears cache")

        mobiles = cache.get('all_mobiles')
        if mobiles is None:
            mobiles = Product.objects.filter(category='M')
            cache.set('all_mobiles', mobiles, CACHE_TTL)
            print("Hit mobiles db")
        else:
            print("Hit mobiles cache")

        laptops = cache.get('all_laptops')
        if laptops is None:
            laptops = Product.objects.filter(category='L')
            cache.set('all_laptops', laptops, CACHE_TTL)
            print("Hit laptops db") 
        else:
            print("Hit laptops cache")

        if request.user.is_authenticated:
            total_item = Cart.objects.filter(user=request.user).count()

        context = {
            'bottomwears':bottomwears,
            'topwears':topwears,
            'mobiles':mobiles,
            'laptops':laptops,
            'total_item':total_item
        }

        return render(request, 'app/home.html', context)



class ProductDetailView(View):
    def get(self, request, pk):
        total_item = 0
        try:
            products = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return HttpResponse("Product not found")
        in_cart = Cart.objects.filter(product__id=pk).exists()
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        context = {
            'products':products, 
            'total_item':total_item,
            'in_cart':in_cart
        }
        return render(request, 'app/productdetail.html', context)



@login_required(login_url='/accounts/login')
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    cart = Cart(user=user, product=product)
    cart.save()
    return redirect('cart')


@login_required(login_url='/accounts/login')
def show_cart(request):
    if request.user.is_authenticated:
        total_item = 0
        user = request.user
        carts = Cart.objects.filter(user=user)
        # print(carts)
        amount = 0.0
        shiping = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))

        if cart_product:
            for p in cart_product:
                tempamount = p.quantity * p.product.price
                amount += tempamount
                totalamount = shiping + amount
            return render(request, 'app/addtocart.html', {'carts':carts, 'totalamount':totalamount, 'amount':amount, 'total_item':total_item})
        else:
            return render(request, 'app/emptycart.html')


@login_required(login_url='/accounts/login')
def update_cart(request, cart_id):
    cart = Cart.objects.get(id=cart_id)
    if request.method == 'POST':
        if request.POST.get('update') == '-1':
            cart.quantity -= 1
            cart.save()
        elif request.POST.get('update') == '1':
            cart.quantity += 1
            cart.save()
    return redirect('cart')



@login_required(login_url='/accounts/login')
def buy_now(request):
    return render(request, 'app/buynow.html')


@method_decorator(login_required(login_url='/accounts/login'), name="dispatch")
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary'})


    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zip_code = form.cleaned_data['zip_code']
            customer = Customer(user=user, name=name, locality=locality, city=city, state=state, zip_code=zip_code)
            customer.save()
            form = CustomerProfileForm()
            messages.success(request, 'Profile Successfuly Updated!')
            return redirect('profile')
        return render(request, 'app/profile.html', {'form':form})


@login_required(login_url='/accounts/login')
def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})


@login_required(login_url='/accounts/login')
def orders(request):
    orderplaced = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'orderplaced':orderplaced})


class MobileView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, data=None):
        if data == None:
            mobiles = Product.objects.filter(category='M')
        elif data == 'Apple' or data == 'Samsung':
            mobiles = Product.objects.filter(category='M').filter(brand=data)
        elif data == 'below':
            mobiles = Product.objects.filter(category='M').filter(price__lt=20000)
        elif data == 'above':
            mobiles = Product.objects.filter(category='M').filter(price__gt=20000)
        context = {
            'mobiles':mobiles
        }
        return render(request, 'app/mobile.html', context)


class LaptopView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, data=None):
        if data == None:
            laptops = Product.objects.filter(category='L')
        elif data == 'Mac' or data == 'Window':
            laptops = Product.objects.filter(category='L').filter(brand=data)
        elif data == 'below':
            laptops = Product.objects.filter(category='L').filter(price__lt=35000)
        elif data == 'above':
            laptops = Product.objects.filter(category='L').filter(price__gt=35000)

        context = {
            'laptops':laptops
        }

        return render(request, 'app/laptop.html', context)


class TopwearView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, data=None):
        if data == None:
            topwears = Product.objects.filter(category='TW')
        elif data == 'Gucci':
            topwears = Product.objects.filter(category='TW').filter(brand=data)
        elif data == 'Prada':
            topwears = Product.objects.filter(category='TW').filter(brand=data)
        elif data == 'below':
            topwears = Product.objects.filter(category='TW').filter(price__lt=500)
        elif data == 'above':
            topwears = Product.objects.filter(category='TW').filter(price__gt=500)
        context = {
            'topwears':topwears
        }

        return render(request, 'app/topwear.html', context)


class BottomwearView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request, data=None):
        if data == None:
            bottomwears = Product.objects.filter(category='BW')
        elif data == 'Gucci':
            bottomwears = Product.objects.filter(category='BW').filter(brand=data)
        elif data == 'Prada':
            bottomwears = Product.objects.filter(category='BW').filter(brand=data)
        elif data == 'below':
            bottomwears = Product.objects.filter(category='BW').filter(price__lt=500)
        elif data == 'above':
            bottomwears = Product.objects.filter(category='BW').filter(price__gt=500)

        context = {
            'bottomwears':bottomwears
        }

        return render(request, 'app/bottomwear.html', context)




class CustomerRegistrationView(View):
    @method_decorator(ratelimit(key='get:q', rate='5/m'))
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    @method_decorator(ratelimit(key='post:q', rate='5/m'))
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            form = CustomerRegistrationForm()
            messages.success(request, 'Successfuly registered!')
            return redirect('login')
        return render(request, 'app/customerregistration.html', {'form':form})


@login_required(login_url='/accounts/login')
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    items = Cart.objects.filter(user=user)
    amount = 0.0
    shiping = 70.0
    cart_product = [p for p in Cart.objects.all() if p.user == user]
    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.price
            amount += tempamount
            totalamount = shiping + amount
        return render(request, 'app/checkout.html', {'add':add, 'items':items, 'totalamount':totalamount})
    return render(request, 'app/checkout.html')



@login_required(login_url='/accounts/login')
def payment_done(request):
    user = request.user
    customer_id = request.GET.get('custid')
    customer = Customer.objects.get(id=customer_id)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        ordersplace = OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity)
        ordersplace.save()
        c.delete()
        return redirect('orders')


@ratelimit(key='get:q', rate='5/m')
@ratelimit(key='post:q', rate='5/m')
def search(request):
    search_query = request.GET.get('query')
    all_item = Product.objects.filter(
        Q(title__contains=search_query)|
        Q(price__contains=search_query)|
        Q(category__contains=search_query)|
        Q(brand__contains=search_query)
    )
    context = {
        'all_item':all_item
    }
    return render(request, 'app/search.html', context)



@login_required(login_url='/accounts/login')
def remove_item(request, id):
    item = Cart.objects.get(id=id)
    item.delete()
    return redirect('cart')



class CommentView(View):
    def get(self, request, *args, **kwargs):
        total_item = 0
        comments = Comment.objects.all().order_by('-created_on') 
        form = CommentForm()
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        context = {
            'form':form,
            'comments':comments,
            'total_item':total_item
        }
        return render(request, 'app/comment.html', context)


    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            comments = Comment.objects.all().order_by('-created_on') 
            form = CommentForm(request.POST)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.author = request.user
                new_post.save()
            context = {
                'form':form,
                'comments':comments
            }
            return render(request, 'app/comment.html', context)
        else:
            return redirect('login')


def about(request):
    total_item = 0
    if request.user.is_authenticated:
        total_item = len(Cart.objects.filter(user=request.user))
    context = {
        'total_item':total_item
    }
    return render(request, 'app/about.html', context)