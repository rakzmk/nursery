from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from user.models import UserDetail, Order
from . models import Categories
from . models import Products
from django.core.files import File
from django.contrib import messages
from django.core.files import File
import base64
from django.core.files.base import ContentFile

# Create your views here.

def adlogin(request):
    if request.session.has_key("setkey"):
        return redirect (adminpanel)
    else:
        if request.method == 'POST':
            usernamead=request.POST['username1']
            passwordad=request.POST['password1']
            print("heeeelo")
            if  usernamead == "admin" and passwordad =="password":
                request.session ['setkey'] = passwordad
                #return redirect(homepage)
                return JsonResponse('true', safe=False)
            else:
                #return render(request,"index.html")
                return JsonResponse('false', safe=False)
        else:
            return render(request, 'admintemp/login.html')


def adminpanel(request):
    if request.session.has_key("setkey"):
        return render(request,'admintemp/dashboard.html')
    
    else:
        return redirect (adlogin)


def userlist(request):

    if request.session.has_key("setkey"):  
        if 'q' in request.GET:     
            q = request.GET['q']
            print(q)
            if q is not None:
                 # user = UserDetail.objects.filter(user__username=q) or UserDetail.objects.filter(user__last_name=q) or UserDetail.objects.filter(user__first_name=q) 
                # for x in user:
                #     print(x.user.first_name)
                user = (UserDetail.objects.filter(user__username__icontains=q)) or (UserDetail.objects.filter(user__first_name__icontains=q)) or (UserDetail.objects.filter(user__last_name__icontains=q)) or (UserDetail.objects.filter(user__email__icontains=q)) or (UserDetail.objects.filter(mobile__icontains=q))
            else:
                user = UserDetail.objects.all()
            return render(request, 'admintemp/userlist.html', {'users': user})
        else:
            user = UserDetail.objects.all()
            return render(request, 'admintemp/userlist.html',{'users': user})

    else:
        return redirect (adlogin)
        #return render(request,"index.html")


def delete_user(request,id):
        if request.method == 'POST':
            pi = UserDetail.objects.get(pk=id)
            pi.delete()
            return redirect('userlist')  



def addproduct(request):
    if request.session.has_key("setkey"):   
        if request.method == 'POST':
            category = request.POST ['category']
            productname = request.POST ['productname']
            price = request.POST ['price']
            description = request.POST ['description']
            
            image1 = request.POST ['imageurl1']
            format, imgstr = image1.split(';base64,')
            ext = format.split('/')[-1]
            img1 = ContentFile(base64.b64decode(imgstr),name=productname+'.'+ ext)
            
            image2 = request.POST ['imageurl2']
            format, imgstr = image2.split(';base64,')
            ext = format.split('/')[-1]
            img2 = ContentFile(base64.b64decode(imgstr),name=productname+'.'+ ext)
            
            image3 = request.POST ['imageurl3']
            format, imgstr = image3.split(';base64,')
            ext = format.split('/')[-1]
            img3 = ContentFile(base64.b64decode(imgstr),name=productname+'.'+ ext)
            
            # image1 = request.FILES.get('image1')
            # image2 = request.FILES.get('image2')
            # image3 = request.FILES.get('image3')
            print(category,productname,price,description)
            categ = Categories.objects.get(category=category)
            
            print (categ.category)
            products = Products.objects.create(product=productname, price=price, description=description, category_id=categ.id, image1=img1,image2=img2,image3=img3)
            products.save()
            return redirect (productlist)
            # return render(request, 'admintemp/addproduct.html')
            # return JsonResponse ('true', safe=False)
        else:
            cat = Categories.objects.all()
            return render(request,'admintemp/addproduct.html',{'category': cat}) 
            # image = request.FILES.get('img')                     
    else:
        return redirect (adlogin)


def productlist(request):
    if request.session.has_key("setkey"):
        prod = Products.objects.all()
        cat = Categories.objects.all()
        return render(request,'admintemp/productlist.html',{'products':prod})
    else:
        return redirect (adlogin)
        #return render(request,"index.html")

def addcategory(request):
    if request.session.has_key("setkey"): 
        if  request.method == 'POST':
            print("reached POST")
            categoryname=request.POST['catname3']
            if Categories.objects.filter(category=categoryname).exists():
                print("username taken")
                return JsonResponse('false', safe=False)
            else:    
                Categories.objects.create(category=categoryname)
                return JsonResponse('true', safe=False)
        else:
            return render(request,'admintemp/addcategory.html')    
    else:
         return redirect(adlogin)
    
        
def delcategory(request,id):
     if request.session.has_key("setkey"):
            # return render(request,"admintemp/categorylist.html")
        
            if request.method =='POST':
                cat = Categories.objects.get(pk=id)
                cat.delete()
                return redirect('categorylist') 
           
     else:
         return redirect(adlogin)

def categorylist(request):
    if request.session.has_key("setkey"):
            
            cat = Categories.objects.all()
            return render(request,'admintemp/categorylist.html',{'category': cat})
        
    else:
        return redirect(adlogin)

def editcategory(request,id):
    if request.session.has_key("setkey"):
        if request.method == 'POST':
            cat=Categories.objects.get(pk=id)
            cat.category = request.POST['name1']
            print("Hello")
            
            if Categories.object.filter(category=cat.category).exclude(id=id).exists():
                print ("hello")
                return JsonResponse('false', safe=False)
            else:
                cat.save()
                return JsonResponse('true', safe=False)
        else:
            pi = Categories.objects.get(pk=id)
            context = {'cat':pi}
            return render(request, 'admin1/categorylist.html',context)  
    else:
        return redirect(adlogin)


def blockuser(request,id): 
    if request.session.has_key("setkey"):  
        user1 = UserDetail.objects.get(id=id)     
        user2 = User.objects.get(id=user1.user_id)
        if user2.is_active==False:
            user2.is_active=True
            user2.save()
            return redirect(userlist)
        else:
            user2.is_active=False
            user2.save()
            return redirect(userlist)
    else:
        return redirect(adlogin)
            
def editproduct(request,id):
    if request.session.has_key("setkey"):
        products = Products.objects.get(pk=id)
        category = Categories.objects.all()
        context = {'prod':products , 'category':category}
        if request.method == 'POST':
            #pro=Products.objects.all(pk=id)
            category1 = request.POST ['category']
            productname = request.POST ['productname']
            price = request.POST ['price']
            description = request.POST ['description']
            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3') 
            #cat.category = request.POST['name1']
            print("Hello")
            categ = Categories.objects.get(category=category1)
            products.category_id = categ
            products.product = productname
            products.price = price
            products.description = description
            products.image1 = image1
            products.image2 = image2
            products.image3 = image3

            if  Products.objects.filter(product=productname).exclude(id=id).exists():
                messages.info(request,"Product name already exists")
            else:
                products.save() 
                return redirect(productlist)
        else:
            return render(request, 'admintemp/editproduct.html', context)  
            

    else:
         return redirect(adlogin)   


def deleteproduct(request,id):
        if request.method == 'POST':
            proddel = Products.objects.get(pk=id)
            proddel.delete()
            return redirect(productlist)

def orderlist(request):
    if request.session.has_key("setkey"):

        order = Order.objects.all()
        context={'order':order}

        return render(request,'admintemp/orderlist.html',context)

def orderstatus(request):
    if request.session.has_key("setkey"):
        if request.method == 'POST':
            orderid = request.POST ['orderid']
            order = Order.objects.get(id=orderid)
            
            if request.POST ['clicked'] == 'Shipped':
                print("hello there I have reached")
                order.status = 'shipped'
                order.save()
                return JsonResponse('true', safe=False)
            elif request.POST['clicked'] == 'Delivered':
                print("hello the")
                order.status = 'delivered'
                order.save()
            return JsonResponse('true', safe=False)




def adlogout(request):
    if request.session.has_key("setkey"):
        request.session.flush()
        return redirect(adlogin)