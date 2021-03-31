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
    path('paymentsuccess/',views.paymentsuccess, name ='paymentsuccess'),
    # path('paypal1/',views.paypal1, name='paypal1'),
    path('paypal/',views.paypal, name='paypal'),
    path('paypalsuccess/',views.paypalsuccess, name = 'paypalsuccess'),
    #path('razorpay/',views.razorpay, name = 'razorpay'),
    path('razorsuccess/',views.razorsuccess,name='razorsuccess'),
    path('razorpaypage/',views.razorpaypage,name='razorpaypage'),
    path('userprofile/', views.userprofile, name = 'userprofile'),
    path('edituserprofile/',views.edituserprofile, name='edituserprofile'),
    path('otp_generate/', views.otp_generate, name='otp_generate'),
    path('otp_validate/', views.otp_validate,name='otp_validate'),
    path('userimage/',views.userimage,name='userimage'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('addtocart2/',views.addtocart2, name='addtocart2'),
    
    # path('paymentrazor/', views.paymentrazor, name='paymentraor'),
    # path('paymentpaypal/', views.paymentpaypal,name='paymentpaypal'),

    
]