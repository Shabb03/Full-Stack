from rest_framework import serializers
from .models import *

class APIUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = APIUser
        fields = ['id','email','username']

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'product_image']

class CartItemsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CartItems
        fields = ['product_id', 'item_price', 'quantity']

class CartSerializer(serializers.HyperlinkedModelSerializer):
    items = CartItemsSerializer(many=True, read_only=True, source='cartitems_set')

    class Meta:
        model = Cart
        fields = ['id', 'user_id', 'items']

class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'date_ordered', 'cart_id', 'user_id', 'total_price', 'address', 'instructions']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIUser
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        passsword = validated_data['password']
        newUser = APIUser.objects.create_user(username=username, email=email, password=passsword)
        newUser.save()
        return newUser

class AddItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ['product_id']
    
    def create(self, validated_data):
        product_id = validated_data['product_id']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            shopping_cart = Cart.objects.filter(user_id=current_user, is_active=True).first()
            if shopping_cart is None:
                shopping_cart = Cart.objects.create(user_id=current_user)
            cart_items = CartItems.objects.filter(product_id=product_id, cart_id=shopping_cart).first()
            if cart_items:
                cart_items.quantity = cart_items.quantity + 1
                cart_items.save()
                return cart_items
            else:
                new_cart_item = CartItems.objects.create(cart_id=shopping_cart, product_id=product_id, quantity=1)
                return new_cart_item

                #return CartItems(cart_id=shopping_cart, product_id=product_id, quantity=0)
            
        else:
            return None

class RemoveItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ['product_id']

    def create(self, validated_data):
        product_id = validated_data['product_id']
        request = self.context.get('request', None)
        if request:
            current_user = request.user
            shopping_cart = Cart.objects.filter(user_id=current_user, is_active=True).first()
            cart_items = CartItems.objects.filter(product_id=product_id, cart_id=shopping_cart).first()
            if cart_items:
                if cart_items.quantity > 1:
                    cart_items.quantity = cart_items.quantity - 1
                    cart_items.save()
                    return cart_items
                else:
                    cart_items.delete()
                    return CartItems(cart_id=shopping_cart, product_id=product_id, quantity=0)
            else:
                return CartItems(cart_id=shopping_cart, product_id=product_id, quantity=0)
                #new_cart_item = CartItems.objects.create(cart_id=shopping_cart, product_id=product_id, quantity=0)
                #return new_cart_item
        else:
            return None 

class CheckoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['cart_id', 'total_price', 'address']

    def create(self, validated_data):
        request = self.context.get('request', None)
        current_user = request.user
        cart_id = validated_data['cart_id']
        shp = validated_data['address']

        cart_id.is_active = False
        cart_id.save()

        show_items = CartItems.objects.filter(cart_id=cart_id)
        total = 0.0
        for item in show_items:
            total += float(item.item_price())
 
        order = Order.objects.create(cart_id = cart_id, user_id = current_user, address = shp, total_price = total)
        new_basket = Cart.objects.create(user_id = current_user) 
        return order