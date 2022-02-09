from django.urls import path
from . import views
from . import forms

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
]