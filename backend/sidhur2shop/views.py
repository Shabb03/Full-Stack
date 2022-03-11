# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import generics
from django.shortcuts import redirect
from .models import *
from django.views.generic import CreateView
from django.contrib.auth import login, logout
from .forms import *
from .serializers import *
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

products = Product.objects.all()

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = APIUser.objects.all()

class AddItemAPIView(generics.CreateAPIView):
    serializer_class = AddItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = CartItems.objects.all()

class RemoveItemAPIView(generics.CreateAPIView):
    serializer_class = RemoveItemSerializer
    permission_classes = [IsAuthenticated]
    queryset = CartItems.objects.all()

class CheckoutAPIView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()

def home(request):
    return render(request, 'home.html', {'products':products})

def product(request, prodid):
    product = Product.objects.get(id=prodid)
    return render(request, 'product.html', {'product':product})

class UserSignupView(CreateView):
    model = APIUser
    form_class = UserSignupForm
    template_name = 'register.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class UserLoginView(LoginView):
    template_name='login.html'

@login_required
def logout_user(request):
    logout(request)
    return redirect("/")

@login_required
def add_item(request, prodid):
    user = request.user
    cart = Cart.objects.filter(user_id=user, is_active=True).first()
    if cart is None:
        Cart.objects.create(user_id = user)
        cart = Cart.objects.filter(user_id=user, is_active=True).first()
    product = Product.objects.get(id=prodid)
    show_items = CartItems.objects.filter(cart_id=cart, product_id = product).first()
    if show_items is None:
        show_items = CartItems(cart_id=cart, product_id = product)
        show_items.save()
    else:
        show_items.quantity = show_items.quantity+1
        show_items.save()
    return render(request, 'product.html', {'product': product, 'added':True})

@login_required
def display_cart(request):
    user = request.user
    cart = Cart.objects.filter(user_id=user, is_active=True).first()
    if cart is None:
        return render(request, 'cart.html', {'empty':True})
    else:
        show_items = CartItems.objects.filter(cart_id=cart)
        if show_items.exists():
            return render(request, 'cart.html', {'cart':cart, 'show_items':show_items})
        else:
            return render(request, 'cart.html', {'empty':True})

@login_required
def remove(request, show_items):
    cartitem = CartItems.objects.get(id=show_items)
    if cartitem is None:
        return redirect('/cart')
    else:
        if cartitem.quantity > 1:
            cartitem.quantity = cartitem.quantity - 1
            cartitem.save()
        else:
            cartitem.delete()
    return redirect('/cart')

@login_required
def order(request):
    user = request.user
    cart = Cart.objects.filter(user_id=user, is_active=True).first()
    if cart is None:
        return redirect('/')
    show_items = CartItems.objects.filter(cart_id=cart)
    if not show_items.exists():
        return redirect('/')
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_id = user
            order.cart_id = cart
            total = 0.0
            for item in show_items:
                total += float(item.item_price())
            order.total_price = total
            order.save()
            cart.is_active = False
            cart.save()
            return render(request, 'fulfilled.html', {'order':order, 'cart':cart, 'show_items':show_items})
        else:
            return render(request, 'orders.html', {'form':form, 'cart':cart, 'show_items':show_items})
    else:
        form = OrderForm()
        return render(request, 'orders.html', {'form':form, 'cart':cart, 'show_items':show_items})

@login_required
def purchases(request):
    user = request.user
    orders = Order.objects.filter(user_id=user)
    return render(request, 'purchases.html', {'orders':orders})

class ProductViewSet(viewsets.ModelViewSet):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Cart.objects.all()
        else:
            shopping_cart = Cart.objects.filter(user_id=user, is_active=True)
            return shopping_cart

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Order.objects.all()
        else:
            orders = Order.objects.filter(user_id=user)
            return orders

class APIUserViewSet(viewsets.ModelViewSet):
    queryset = APIUser.objects.all()
    serializer_class = APIUserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

