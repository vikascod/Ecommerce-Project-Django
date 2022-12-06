from django.shortcuts import render, redirect
from app.models import Product, Cart, Customer, OrderPlaced, Comment
from django.views.generic import View
from app.forms import CustomerRegistrationForm, LoginForm, CustomerProfileForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q


class ProductView(View):
    def get(self, request, *args, **kwargs):
        total_item = 0
        bottomwears = Product.objects.filter(category='BW')
        topwears = Product.objects.filter(category='TW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
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
        products = Product.objects.get(pk=pk)
        in_cart = Cart.objects.filter(product__id=pk).exists()
        if request.user.is_authenticated:
            total_item = len(Cart.objects.filter(user=request.user))
        context = {
            'products':products, 
            'total_item':total_item,
            'in_cart':in_cart
        }
        # item_already_in_cart = False
        # item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html', context)

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    cart = Cart(user=user, product=product)
    cart.save()
    return redirect('cart')


@login_required
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



@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')


@method_decorator(login_required, name="dispatch")
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



def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html', {'add':add, 'active':'btn-primary'})


@login_required()
def orders(request):
    orderplaced = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'orderplaced':orderplaced})


class MobileView(View):
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
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            form = CustomerRegistrationForm()
            messages.success(request, 'Successfuly registered!')
            return redirect('login')
        return render(request, 'app/customerregistration.html', {'form':form})


@login_required
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

@login_required()
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



@login_required()
def remove_item(request, id):
    item = Cart.objects.get(id=id)
    item.delete()
    return redirect('cart')


class CommentView(View):
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.all().order_by('-created_on') 
        form = CommentForm()
        context = {
            'form':form,
            'comments':comments
        }
        return render(request, 'app/comment.html', context)
    
    def post(self, request, *args, **kwargs):
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
