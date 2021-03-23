from django.urls import path
from . import views

urlpatterns = [
    path('',views.mainpage, name='index'),
    path('login/',views.login , name='login'),
    path('register/',views.register, name='register'),
    path('logout/',views.logout, name='logout'),
    path('usershop/',views.usershop, name='usershop'),
    path('menubar/<int:id>',views.menubar, name='menubar'),
    path('usercart/',views.usercart, name='usercart'),
    path('usergallery/',views.usergallery,name='usergallery'),
    path('productdetail/<int:id>',views.productdetail, name='productdetail'),
    path('seedshop/<int:id>', views.seedshop, name='seedshop'),
    path('addtocart/<int:id>',views.addtocart, name = 'addtocart'),
    path('deletecartprod/<int:id>',views.deletecartprod,name = 'deletecartprod'),
    path('updatecartplus/',views.updatecartplus,name='updatecartplus'),
    path('updatecartminus/',views.updatecartminus,name='updatecartminus'),
    path('checkout/',views.checkout, name='checkout'),
    path('checkoutaddress/',views.checkoutaddress,name='checkoutaddress'),
    path('deleteaddress/<int:id>',views.deleteaddress, name = 'deleteaddress'),
    path('checkoutadd/<int:id>',views.checkoutadd, name='checkoutadd'),
    path('paymentpage/',views.paymentpage, name='paymentpage'),

    
]