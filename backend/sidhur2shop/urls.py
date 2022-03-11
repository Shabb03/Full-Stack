from django.urls import path
from . import views
from . import forms
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'cart', views.CartViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'users', views.APIUserViewSet)

urlpatterns = [
    path('', views.home, name="homepage"),
    path('register/', views.UserSignupView.as_view(), name="register"),
    path('products/<int:prodid>', views.product, name="product"),
    path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=forms.UserLoginForm)),
    path('logout/', views.logout_user, name="logout"),
    path('addbasket/<int:prodid>', views.add_item, name="add_item"),
    path('cart/', views.display_cart, name="display_cart"),
    path('remove/<int:show_items>', views.remove, name='remove_item'),
    path('order/', views.order, name="order"),
    path('history/', views.purchases, name="history"),
    path('api/', include(router.urls)),
    path('apiregister/', views.UserRegistrationAPIView.as_view(), name="api_register"),
    path('apiadd/', views.AddItemAPIView.as_view(), name="api_add_to_basket"),
    path('apiremove/', views.RemoveItemAPIView.as_view(), name="api_remove_from_basket"),
    path('apicheckout/', views.CheckoutAPIView.as_view(), name="api_checkout"),
]