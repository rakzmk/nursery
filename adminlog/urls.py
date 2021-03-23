from django.urls import path
from . import views


urlpatterns = [
    path('',views.adlogin,name='adlogin'),
    path('adminpanel/',views.adminpanel, name = 'adminpanel'),
    path('userlist/',views.userlist, name='userlist'),
    path('deleteuser/<int:id>',views.delete_user, name='delete_user'),
    path('addproduct/',views.addproduct, name='addproduct'),
    path('productlist/',views.productlist, name='productlist'),
    path('addcategory/',views.addcategory, name='addcategory'),
    path('delcategory/<int:id>',views.delcategory, name='delcategory'),
    path('categorylist/',views.categorylist, name='categorylist'),
    path('editcategory/<int:id>',views.editcategory, name='editcategory'),
    path('blockuser/<int:id>',views.blockuser, name='blockuser'),
    path('editproduct/<int:id>',views.editproduct, name='editproduct'),
    path('deleteproduct/<int:id>',views.deleteproduct,name='deleteproduct'),
    path('adlogout/',views.adlogout,name='adlogout')
    
]