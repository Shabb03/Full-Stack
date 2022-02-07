from django.urls import path
from . import views
from . import forms

urlpatterns = [
   #path('', views.index, name="index"),
   path('', views.index, name="homepage"),
   path('register/', views.UserSignupView.as_view(), name="register"),
   path('products/<int:prodid>', views.product_individual, name="individual_product"),
   path('login/',views.LoginView.as_view(template_name="login.html", authentication_form=forms.UserLoginForm)),
   path('logout/', views.logout_user, name="logout"),
   path('addbasket/<int:prodid>', views.add_to_basket, name="add_basket"),
   path('basket/', views.show_basket, name="show_basket")
]