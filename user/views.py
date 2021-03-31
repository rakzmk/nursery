from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from user.models import UserDetail
from adminlog.models import Categories, Products
from .models import Cart, Address, Order
from django.views.decorators.csrf import csrf_exempt
#import razorpay
import os
import random
from twilio.rest import Client
from django.contrib.auth.hashers import check_password


otp = 0
phone_number = 0
total_incart = 0

# Create your views here.

def mainpage(request):
    
    # if request.user.is_active == False:
    #     cat = Categories.objects.all()
    #     return render(request,'usertemp/index.html',{'category': cat})
    if request.user.is_active == True and request.user.is_authenticated:
        cat = Categories.objects.all()
        cart = Cart.objects.filter(user=request.user)
        cart = Cart.objects.filter(user_id=request.user)
        
       
       
        context = {'cart': cart ,'category': cat}
        return render(request,'usertemp/index.html',context)
    else:
         cat = Categories.objects.all()
        #  cart = Cart.objects.filter(user=request.user)
         context = {'category': cat}
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
              
        category = Categories.objects.all()
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
        if not user_cart:
            messages = "Your cart is Empty, Please add items to continue."
            cat = Categories.objects.all()
            product = Products.objects.all()
            
            
            category = Categories.objects.all()
            context = {'messages':messages,'product':product,'category': cat}
            
        else:
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
            print("hello this is ",user_cart)
            #if user_cart == isnull:
            #print ("iam hereeee")
            #return redirect (usershop)
            
           # else:
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
                cart=total_price
                sub_total = sub_total + total_price
                grand_total = sub_total - disc - coupon_disc
                
               
            user_obj = request.user
            user = Cart.objects.filter(user=user_obj)
            product = Products.objects.all()
            cat = Categories.objects.all()
            address = Address.objects.filter(user=request.user)
            context = {'address':address,'coupon_disc':coupon_disc,'tax':tax,'shipping':shipping, 'product':product,'category': cat,'cart': user, 'sub_total':sub_total,'grand_total':grand_total, 'user_cart':user_cart,'disc':disc}
            return render(request,'usertemp/checkout.html',context)
          
           
    else:
    
        return redirect (login)
    
@csrf_exempt
def checkoutadd(request,id):
    if request.user.is_authenticated:
        if request.user.is_active == True:
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
            
            Address.objects.create(user=request.user,house_name=house,street_name=street,city=city,district=district, state=state,pincode=pincode,address_mobile=mobile,address_name=name)
            return JsonResponse('false', safe=False)
            
        else:
            # address=Address.objects.all()
            address=Address.objects.filter(user=request.user)
            context={'address':address }
            return render(request,"user/checkout.html", context)
             
                
    
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
    if request.user.is_authenticated:
        category = Categories.objects.all()
        product = Products.objects.filter(category=category)
        
        category = Categories.objects.all()
        context = {"product": product, 'category':category}
        return render (request, 'usertemp/usergallery.html',context)
    
    else:
        category = Categories.objects.all()
        product = Products.objects.filter(category=category)
        
        category = Categories.objects.all()
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
            cod = request.POST['cod']
            grand_total = request.POST['grand_total']
            request.session ['grand_total'] = grand_total

            value1 = request.session ['checkoutadd']
            address=Address.objects.get(id=value1)
            cart = Cart.objects.filter(user_id=address.user_id)
            for cart in cart:
                price=cart.count*cart.product.price
                status = 'ordered'
                Order.objects.create(user_id=request.user, product=cart.product, address=address, price=price, payment_method=cod, status=status, count=cart.count)
                cart.delete()
        return JsonResponse ('true',safe=False)

    else:
        print("not reached")
            
        
def paymentsuccess(request):
    if request.user.is_authenticated:
        value = request.session ['checkoutadd']
        address=Address.objects.get(id=value)
       # orders = Orders.objects.get(id=value)
        cat = Categories.objects.all()
        product = Products.objects.all()
        context = {'product':product,'category': cat,'address':address }
        return render(request, 'usertemp/paymentsuccess.html',context)

# @csrf_exempt
# def paypal1(request):  
#     if request.user.is_authenticated and request.user.is_active == True:
#         if request.method == 'POST':
#             value = request.POST['grand_total']
#             request.session['grand_total'] = value
#             print(value)
#             return JsonResponse ('true', safe=False)
#             #return render (request, 'usertemp/login.html')  

def paypal(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            return JsonResponse('true', safe=False)
        
   
            
    else:
       return redirect (login)

def paypalsuccess(request):
    if request.user.is_authenticated:
        #if request.method == 'POST':
        value1 = request.session ['checkoutadd']
        address=Address.objects.get(id=value1)
        cart = Cart.objects.filter(user_id=address.user_id)
        paypal = 'paypal'
        status = 'ordered'
        print("reached here buddyyyy")
        for cart in cart:
            price=cart.count*cart.product.price
            Order.objects.create(user_id=request.user, product=cart.product, address=address, price=price, payment_method=paypal, status=status, count=cart.count)
            cart.delete()
    
        value = request.session ['checkoutadd']
        address=Address.objects.get(id=value)
        print("hello this th place")
        return render(request,'usertemp/paypalsuccess.html', {'address':address}) 
        # return JsonResponse('true', safe=False)

@csrf_exempt
def razorpaypage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
           
            #return render (request, 'usertemp/index.html', {'value':value})
            return JsonResponse('true',safe=False)

def razorsuccess(request):
    if request.user.is_authenticated:
        #if request.method == 'POST':
            #cod = request.POST['cod']
            #grand_total = request.POST['grand_total']
            #request.session ['grand_total'] = grand_total

            value1 = request.session ['checkoutadd']
            address=Address.objects.get(id=value1)
            cart = Cart.objects.filter(user_id=address.user_id)
            razor = 'razor_pay'
            status = 'ordered'
            for cart in cart:
                price=cart.count*cart.product.price
                Order.objects.create(user_id=request.user, product=cart.product, address=address, price=price, payment_method=razor, status=status, count=cart.count)
                cart.delete()
       
            value = request.session ['checkoutadd']
            address=Address.objects.get(id=value)
            print("hello this th place")
            return render(request,'usertemp/razorsuccess.html', {'address':address})    
            #return JsonResponse ('true',safe=False)


def userprofile(request):
    if request.user.is_authenticated:
        user1 = User.objects.get(id=request.user.id)
        user2 = UserDetail.objects.get(user=user1)
        value = Order.objects.filter(user_id=user1)
        cat = Categories.objects.all()
        product = Products.objects.all()
        category = Categories.objects.all()
        context = {'user2':user2,'user1':user1,'messages':messages,'product':product,'category': cat,'value':value}
        return render(request, 'usertemp/userprofile.html',context)
    else:
        return redirect(mainpage)   
        
def userimage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user1 = request.user
            image1 = request.FILES.get('image1')
            user = UserDetail.objects.get(user_id=user1)
            user.user_image1 = image1
            user.save()
            return redirect('userprofile')
            




def edituserprofile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = User.objects.get(username=request.user)
            user1 = UserDetail.objects.get(user_id=user)
            user.first_name = request.POST ['name']
            user.last_name = request.POST ['lname']
            user.email = request.POST ['email']
            user1.mobile = request.POST['mobile']
           # user.username = method.POST['username']
            print(user.first_name,user.last_name,user.email)
            print("reached here safely")
            #if User.objects.filter(username=user.username).exclude(request.user).exists():
                #return JsonResponse('false', safe=False)
            if User.objects.filter(email=user.email).exclude(username=request.user).exists():
                print("false")
                return JsonResponse('false', safe=False)
            elif UserDetail.objects.filter(mobile=user1.mobile).exclude(user=request.user).exists():
                print("false1")
                return JsonResponse('false1', safe=False)
            else:
                 
                user.save()
                user1.save()
                print("true")
                return JsonResponse('true', safe=False)
    else:
        return redirect (login)


def changepassword(request):
    if request.user.is_authenticated:
        user = request.user
        user1 = User.objects.get(username=user)
        
        if request.method == 'POST':
            pwd = request.POST ['pwd']
            newpwd = request.POST ['newpwd']
            #conpwd = method.POST ['conpwd']
            oldpassword = request.user.password
            passwdchk = check_password(pwd,oldpassword)
        
            if passwdchk != True:
                return JsonResponse('false', safe=False)
            else: 
                user.set_password(newpwd)
                user.save()
                return JsonResponse('true',safe=False)


        else:
            cat = Categories.objects.all()
            product = Products.objects.all()
            category = Categories.objects.all()
            context = {'product':product,'category': cat}
            return render(request,'usertemp/changepassword.html',context)
    
    else:
        return redirect (login)



def otp_generate(request):
    #return render (request,'usertemp/loginmobile.html')
    if request.method == 'POST':
        phone_number = request.POST['mobile']
        if UserDetail.objects.filter(mobile= phone_number).exists():
            user1 = UserDetail.objects.get(mobile= phone_number)
            #baseuser = user1.user
            #print("helooo",baseuser)
            request.session['phone'] = phone_number
            if user1 is not None:
                random_number = random.randint(1000, 9999)
                global otp
                otp = random_number
                print(otp)
                account_sid ='AC470f5283fa04d03253312e5df5e3a0bc'
                auth_token = '6465318935c483a411c670e4941de3ff'
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    body = f"Your OTP is {otp}",
                    from_ = '+12037796637',
                    to=f'+918590719050'
                )

                #context = {'user':user1}
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return JsonResponse('false1', safe=False)
            
    else:
        return render (request,'usertemp/loginmobile.html')

def otp_validate(request):
    if request.method == 'POST':
        print("reached herre")
        phone = request.session['phone']
        user1 = UserDetail.objects.get(mobile=phone)
        print("reached herre mobilr")
        baseuser = user1.user
        user_otp = request.POST ['otp']
        print(user_otp)
        global otp
        print(user_otp)
        if otp == int(user_otp):
            auth.login(request, baseuser)
            print("reached herre monnmn")
            return JsonResponse ('true', safe=False)
        else:
            return JsonResponse ('false', safe=False)
            
    else:
        return render(request,'usertemp/loginmob_otp.html')

def addtocart2(request):
    if request.method =='POST':
        qty = request.POST['qty']
        id3 = request.POST['id3']
        print("reached hereeee")
        cartprod = Products.objects.get(pk=id3)
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