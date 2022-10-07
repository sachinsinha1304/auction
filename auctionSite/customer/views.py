from django.shortcuts import render,redirect
from .models import *
from django.utils import timezone
from django.db.models import Avg
from .forms import *

# for nlp dynamic rating
import os
import pickle5 as pickle
import preprocess_kgptalkie as ps
import re
# ...................

import random

# preprocessing comments
def get_clean(x):
  x = str(x).lower().replace('\\', '').replace('_', ' ')
  x = ps.cont_exp(x)
  x = ps.remove_emails(x)
  x = ps.remove_urls(x)
  x = ps.remove_accented_chars(x)
  x = ps.remove_special_chars(x)
  x = re.sub("(.)\\1{2,}", "\\1", x)
  return x
# .......................

# Create your views here.

# home page
def index(request):
    name = None
    try:
        email = request.session.get('email')
        mode = request.session.get('mode')
        obj = userDetails.objects.filter(email = email)
        name = obj[0].name
        print(name)
    except:
        pass

    if request.method == 'POST':
        postVal = request.POST
        print(postVal.get('product'))
    

    cat = Category.objects.all()
    data = item.objects.filter(status = False)
    sold = SoldItems.objects.all()
    print(sold)

    if request.GET.get('category'):
        data = item.objects.filter(category = int(request.GET.get('category')), status = False)

    return render(request,'index.html',{'data':data,'category':cat,'sold':sold,'name':name,'mode':mode})

# .....................................

def describe(request,val):

    if request.method == 'POST':
        postVal = request.POST
        price = None
        message = None
        try:
            price = postVal['bid']
        except:
            print('hello bid',price)
        
        try:
            message = postVal['message']
        except:
            print('hello mesage')

        

        if message:
            if os.path.exists('customer//train_model.pickle'):
                print('loading model')
                m1 = pickle.load(open('customer//train_model.pickle','rb'))

            if os.path.exists('customer//train_model_analyser.pickle'):
                print('loading model')
                m2 = pickle.load(open('customer//train_model_analyser.pickle','rb'))

            x = get_clean(message)

            vec = m1.transform([x])
            rat = m2.predict(vec)
            print(rat)

            obj = Comments(comment = message, product = item.objects.get(id = val),rating = rat)
            obj.save()
        
        elif request.session.get('email'):
            email = request.session.get('email')
            Id = userDetails.objects.get(email = email)

            if Biddings.objects.filter(itemId = val , custId = Id.id):
                b = Biddings.objects.filter(itemId = val , custId = Id.id)[0]
                if price != None and b.bidd < int(price):
                    b.bidd = price
                    b.save()
                else:
                    print('incorrect')
            else:
                obj = Biddings(itemId = item.objects.filter(id = val)[0], custId = Id, bidd = price)
                obj.save()

        else:
            return redirect(login)


    message = Comments.objects.filter(product = val)
    data = item.objects.filter(id = val)
    maxBid = Biddings.objects.filter(itemId = val).order_by('-bidd')
    res = message.aggregate(Avg('rating'))
    res = res['rating__avg']
    print(res)

    if len(maxBid) > 0:
        maxBid = maxBid[0]

    else:
        maxBid = 'There are no bids currently'

    return render(request,'describe.html',{'data':data, 'bidd':maxBid, 'message' : message ,'res':res})


def login(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        passwd = request.POST.get('psw')
        buyer = request.POST.get('buyer')

        if buyer == 'on':
            buyer = True
        else:
            buyer = False

        if userDetails.objects.filter(email = name, password=passwd):
            request.session['email'] = name
            request.session['mode'] = buyer
            return redirect(index)
        else:
            return render(request,'login.html',{'status':'wrong credentials'})

    return render(request,'login.html')

def signUp(request):

    if request.method == 'POST':
        postVal = request.POST
        name = postVal.get('name')
        phone = postVal.get('phone')
        email = postVal.get('email')
        sex = postVal.get('sex')
        mode = postVal.get('mode')
        psw = postVal.get('psw')
        psw_repeat = postVal.get('psw_repeat')

        


        '''validation for credentials'''

        error = None
        if not name:
            error = 'Name is missing'
        elif len(name) < 3:
            error = 'Invalid name'

        elif len(str(phone)) != 10:
            error = 'Invalid Phone Number'

        elif len(psw) < 5:
            error = "weak password"


        elif psw != psw_repeat:
            error = 'repeated password is incorrect'


        else:
            if mode == 'on':
                mode = True
            else:
                mode = False

            if sex == 'on':
                sex = True
            else:
                sex = False

                
            obj = userDetails(name = name, email = email, contact = phone, gender=sex, mode= mode, password = psw)
            obj.save()

            return redirect(login)

        value = {'name':name, 'phone':phone,'email':email,'sex':sex,'mode':mode,'error':error}

        if error != None:
            return render(request,'signUp.html', value)
            
            
    return render(request,'signUp.html')


def logout(request):
    request.session.clear()
    return redirect(login)

def bid(request):
    email = request.session.get('email')
    Id = userDetails.objects.filter(email = email)[0]

    val = {}

    obj = Biddings.objects.filter(custId = Id)


    return render(request, 'bid.html',{"obj":obj})

def addItem(request):
    if request.method == 'POST':
        form = HotelForm(request.POST, request.FILES)
  
        if form.is_valid():
            form.save()
            print('heloo')
    else:
        form = HotelForm()
        print('hello')
    return render(request, 'check.html', {'form' : form})

def removingItem():
    now = timezone.now()	


    # day = date.today()
    data = item.objects.filter(closingDate__lte =  now,status = False)
    
    for i in data:
        print(i)
        # getting the object with greatest bid
        obj = Biddings.objects.filter(itemId = i.id).order_by("-bidd")[:1]

        # now storing the data in SoldItems table
        
        if obj:
            for val in obj:
                pr = val.bidd
                cust_id = val.custId

            s = SoldItems(itemId = i, custId = cust_id, price = pr)
            s.save()

            # changing status of item as sold
            file = item.objects.get(id = i.id)
            file.status = True
            file.save()

            # to removing the bids made on said item
            Biddings.objects.filter(itemId = i.id).delete()

        else:
            print('cant be sold')

def password(request):
    if request.method == 'POST':
        val = request.POST
        email = val.get('email')
        
        # request.session['email'] = email
        otp = random.randint(10000,99999)
        request.session['otp'] = otp
        print(otp)
        return redirect(changePassword)

    return render(request,'password.html')

def changePassword(request):
    # email = request.session['email']
    message = None
    otp = request.session['otp']

    if request.method == 'POST':

        val = request.POST
        email = val.get("email")
        userOtp = val.get("otp")
        psw = val.get("psw")
        psw_repeat = val.get("psw_repeat")
        if otp == int(userOtp):
            if psw == psw_repeat:
                obj = userDetails.objects.get(email = email)
                obj.password = psw
                obj.save()
                request.session.clear()
                return redirect(index)
                
            else:
                message = 'password dont match'

        else:
            message = 'incorrect otp'
        

    return render(request,'changePassword.html', {'message' : message})
    
    



  

  
    

        

    