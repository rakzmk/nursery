from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from user.models import UserDetail
from adminlog.models import Categories, Products
from user.models import Cart, Address, Order
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def mainpage(request):
    
    # if request.user.is_active == False:
    #     cat = Categories.objects.all()
    #     return render(request,'usertemp/index.html',{'category': cat})
    if request.user.is_active == True and request.user.is_authenticated:
        cat = Categories.objects.all()
        cart = Cart.objects.all()
        context = {'cart': cart ,'category': cat}
        return render(request,'usertemp/index.html',context)
    else:
         cat = Categories.objects.all()
         cart = Cart.objects.all()
         context = {'cart': cart ,'category': cat}
         return render(request,'usertemp/index.html',context)

    


def login(request):  
    if request.user.is_authenticated:
         return redirect(mainpage)
                  
    else:  
        if request.method == 'POST':
            username2=request.POST['name2']
            #email2=request.POST['email2']
            password2=request.POST['password2']
            if User.objects.filter(username=username2).exists() or User.objects.filter(username=username2).exists():
                user = (User.objects.get(username=username2)) or (User.objects.get(password=password2))
                if user.is_active==False:
                    return JsonResponse('blocked',safe=False)
                else:
                    user = auth.authenticate(username=username2,password=password2) 
                    if user is not None:
                        auth.login(request,user)
                        return JsonResponse('true', safe=False)
                    else:
                        return JsonResponse('false',safe=False)
            else:
                return JsonResponse('false', safe=False)
                       
        else:
            cat = Categories.objects.all()
            return render(request,'usertemp/login.html',{'category': cat})
               

        


def register(request):
        if request.user.is_authenticated:
            return redirect(mainpage)
        else:
            if request.method == 'POST':
                first_name=request.POST['name3']
                last_name=request.POST['lname3']
                email=request.POST['email3']
                mobile=request.POST['mobile3']
                username1=request.POST['username3']
                password1=request.POST['pwd3']
                #password2=request.POST['cpwd3']
                if User.objects.filter(username=username1).exists():
                    return JsonResponse('false', safe=False)
                elif User.objects.filter(email=email).exists():
                    return JsonResponse('false1', safe=False)

                else:    
                    userr =  User.objects.create_user(username=username1, last_name=last_name, password=password1,email=email,first_name=first_name)
                    UserDetail.objects.create(user=userr,mobile=mobile)
                    return JsonResponse('true', safe=False)
        
            else:
                return render(request,'usertemp/register.html') 

def usershop(request):
    #if request.user.is_authenticated:
            cat = Categories.objects.all()
            prod= Products.objects.all()
            context = {'category':cat, 'product':prod}
            return render(request, 'usertemp/usershop.html', context)

           

    #else:
        #return redirect(mainpage)

def seedshop(request,id):
        if id==9:
            cat = Categories.objects.get(pk=id)
            product = Products.objects.filter(category=cat)
            category = Categories.objects.all()
            context = {"product": product,'category': category}
            return render(request, 'usertemp/usershopseeds.html', context)
        
        elif id == 10 :
            cat = Categories.objects.get(pk=id)
            product = Products.objects.filter(category=cat)
            category = Categories.objects.all()
            context = {"product": product,'category': category}
            return render(request, 'usertemp/usershopplanters.html', context)
        

def logout(request):
    auth.logout(request)
    return redirect(mainpage)


def menubar(request,id):
    #if request.user.is_authenticated: 
        category = Categories.objects.all()
        cat = Categories.objects.get(pk=id)
        product = Products.objects.filter(category=cat)
        context = {"product": product,'category': category}
        return render(request, 'usertemp/usershop.html',context)
        # if cat == 'Seeds' and cat == 'Planters':
        #     product = Products.objects.filter(category=cat)
        #     return render(request,'usertemp/usershop.html',{'category': cat})
        # else:
        #     category = Categories.objects.all()
        #     cat = Categories.objects.get(pk=id)
        #     product = Products.objects.filter(category=cat)
        #     context = {"product": product,'category': category}
        #     return render(request,'usertemp/usershop.html',context)


def usercart(request):
    if request.user.is_active == True and request.user.is_authenticated:
        user_cart = Cart.objects.filter(user=request.user)
        # if  not user_cart:
        #     messages = "Your cart is Empty"
        # else:
        user_cart = Cart.objects.filter(user=request.user)
        sub_total=0
        disc=0
        coupon_disc=0
        tax=0
        shipping=0
        total_price = 0
            #disc_sub_total = 0
        grand_total = 40
        for cart in user_cart:
            qty = cart.count
            price = cart.product.price
            total_price = qty * price
            cart.total_price = total_price
            sub_total = sub_total + total_price
            
            grand_total = sub_total - disc - coupon_disc
            # context = {cat}
        user_obj = request.user
        user = Cart.objects.filter(user=user_obj)
        product = Products.objects.all()
        cat = Categories.objects.all()
          
        context = {'coupon_disc':coupon_disc,'total_price':total_price, 'tax':tax,'shipping':shipping, 'product':product,'category': cat,'cart': user, 'sub_total':sub_total,'grand_total':grand_total, 'user_cart':user_cart,'disc':disc}
        return render(request,'usertemp/usercart.html',context)
        
    else:
        cat = Categories.objects.all()
        product = Products.objects.all()
        context = {'product':product,'category': cat}
        return render(request,'usertemp/login.html',context)
            
def checkout(request):
    if request.user.is_authenticated:
            user_cart = Cart.objects.filter(user=request.user)
            sub_total=0
            disc=0
            coupon_disc=0
            tax=0
            shipping=0
            grand_total = 40
            for cart in user_cart:  
                qty = cart.count
                price = cart.product.price
                total_price = qty * price
                sub_total = sub_total + total_price
                grand_total = sub_total - disc - coupon_disc
                
               
            user_obj = request.user
            user = Cart.objects.filter(user=user_obj)
            product = Products.objects.all()
            cat = Categories.objects.all()
            address = Address.objects.all()
            context = {'address':address,'coupon_disc':coupon_disc,'tax':tax,'shipping':shipping, 'product':product,'category': cat,'cart': user, 'total_price':total_price, 'sub_total':sub_total,'grand_total':grand_total, 'user_cart':user_cart,'disc':disc}
            return render(request,'usertemp/checkout.html',context)
            


            #user1 = Cart.objects.all()
            #cart = Cart.objects.all()
           
            #return render (request, 'usertemp/usercart.html')
       # else:
             #return redirect (checkout)
           
    else:
    
        return redirect (login)
    
@csrf_exempt
def checkoutadd(request,id):
    if request.user.is_authenticated:
        if request.user.is_active == True:
            #request.method=='POST'
            request.session['checkoutadd'] = id
            return JsonResponse('true', safe=False)
        else:
            return redirect (login)
    else:
        return redirect (login)


def checkoutaddress(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name=request.POST['name']
            house=request.POST['house']
            street=request.POST['street']
            city = request.POST['city']
            district = request.POST['district']
            state = request.POST['state']
            pincode = request.POST['pincode']
            mobile = request.POST['mobile']
            
            #if Address.objects.filter(user=request.user).count() == 3:
                
            Address.objects.create(user=request.user,house_name=house,street_name=street,city=city,district=district, state=state,pincode=pincode,address_mobile=mobile,address_name=name)
            return JsonResponse('false', safe=False)
            
        else:
            address=Address.objects.all()
            context={'address':address }
            return render(request,"user/checkout.html", context)
            #Address.objects.filter(user=request.user):
            #    address = Address.objects.get(user=request.user)
             #   address.save()    
              #  return JsonResponse('true', safe=False)      
                
    
    else:
        return redirect(login)


def deleteaddress(request,id):
    if request.user.is_authenticated:
        user=Address.objects.filter(id=id)
        user.delete()
        return redirect(checkout)






def updatecartplus(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            cart_id = request.POST['cart_id']
            qty = request.POST['qty']
            count = Cart.objects.get(id=cart_id)
            count.count = count.count + 1
            count.save()
            return JsonResponse('true', safe=False) 
        else:
            if qty == 20:  
                return JsonResponse('false', safe=False)
    
    else:
            return redirect (login)



def updatecartminus(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            cart_id = request.POST['cart_id']
            qty = request.POST ['qty']
            #if int(qty) >= 0:
                #return JsonResponse('false', safe=False)
            #if:
            count = Cart.objects.get(id=cart_id)
            count.count = count.count - 1
            if count.count == 0:
                return JsonResponse('false', safe=False)
                    
            else:
                   # count = Cart.objects.get(id=cart_id)
                   # count.count = count.count - 1
                count.save()    
                return JsonResponse('true', safe=False)
                  
                #return JsonResponse('true', safe=False)






            # cart = Cart.objects.get(id=cart_id)
            # add = Cart.objects.get(id=cart_id)
            # add.count = add.count + 1
            # add.save()
            # return JsonResponse('true', safe=False)
        # add = Cart.objects.filter(user=request.user)
        # if Cart.objects.filter(id=cart, user=request.user).exists():
        #     add = Cart.objects.get(poduct=cart)
        #     add.count = add.count + 1
        #     add.save()
        
        # else:
        #     return JsonResponse('false', safe=False)
    else:
        return redirect (login)





def deletecartprod(request,id):
     if request.user.is_authenticated:
            # return render(request,"admintemp/categorylist.html")
            if request.method =='POST':
                cart = Cart.objects.get(pk=id)
                cart.delete()
                return redirect('usercart') 
            else:
                return redirect(usercart)
           
     else:
         return redirect(login)







def usergallery(request):
        category = Categories.objects.all()
        product = Products.objects.filter(category=category)
        context = {"product": product, 'category':category}
        return render (request, 'usertemp/usergallery.html',context)


def productdetail(request,id):
        # cat = Categories.objects.get(pk=id)
        product = Products.objects.get(pk=id)
        # product = Products.objects.filter(category=cat)
        category = Categories.objects.all()
        context = {"product": product, 'category':category}
        return render(request,'usertemp/productdetail.html',context)
    
    
def addtocart(request,id):
    if request.user.is_active == True and request.user.is_authenticated:
                if request.method =='POST':
                    qty = request.POST['qty']
                    cartprod = Products.objects.get(pk=id)
                    #products = Products.objects.filter(product=cartprod)
                    if Cart.objects.filter(product=cartprod, user=request.user).exists():
                        add = Cart.objects.get(product=cartprod, user=request.user)
                        add.count = add.count + int(qty)
                        add.save()
                        return JsonResponse('true', safe=False)
                    else:
                        Cart.objects.create(count=qty, product=cartprod,user=request.user)
                        return JsonResponse('false', safe=False)
                else:
                    return redirect(login)
    else:
        return redirect(login)


@csrf_exempt
def paymentpage(request):
    if request.user.is_active == True and request.user.is_authenticated:
        if request.method == 'POST':
            tryr= request.POST['value']
            value1 = request.session ['checkoutadd']
            print("hello this is session", value1)
            address=Address.objects.get(id=value1)
            print(address.address_name, address.user_id)
            print ("reached here buddy", )
            return render (request,'usertemp/paymentpage.html')
        else:
            print("not reached")
            # cart= Cart.objects.filter(usser_id=address)
            #Address.objects.create(user=request.user,house_name=house,street_name=street,city=city,district=district, state=state,pincode=pincode,address_mobile=mobile,address_name=name)      
        

            
               
            
           
        
        
    
        

          
