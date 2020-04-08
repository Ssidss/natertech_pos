from django.shortcuts import render, redirect
from StockSystem import models, forms
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime 
from django.contrib.sessions.models import Session

def index_page(request):
    return render(request, 'index.html', locals())

def product_list(request):
    try:
        Product_all = models.Product.objects.all()
        print("all success")
    except Exception as e:
        print(e)
    return render(request, 'product_list.html', locals())


def product_view(request, p_num = None):
    ProductForm = forms.Product()
    Productcontext = models.Product()
    if request.method == 'GET':
        try:
            Productcontext = models.Product.objects.get(product_num = p_num)
            ProductForm = forms.Product(instance= Productcontext) #instance -> 讀取裡面的東西
            #ProductForm.Meta.model.objects.get(product_num = p_num)
            #NameTitle = Productcontext.name
            #print(ProductForm.as_table)
            print("get success")
        except:
            print("search fail")
    elif request.method == 'POST':
        try:
            Productcontext = models.Product.objects.get(product_num = p_num)
            ProductForm = forms.Product(request.POST, instance = Productcontext)
            if ProductForm.is_valid():
                #Productcontext = models.Product.objects.get(product_num = ProductForm.fields['product_num'])
                #Productcontext.amount = ProductForm.fields['amount']
                Productcontext.save()
            print("post success")
        except:
            print("post fail")
    #return JsonResponse(locals())
    return render(request, 'product_detail.html', locals())

def purchase_page(request, product_num = None):
    # If request method is Get
    Product = models.Product.objects.get(product_num = product_num)
            # Create Purchase Form 
    PurchaseForm = forms.Purchase(initial = {'product': Product})
    if request.method == 'GET':
        try: 
            pass
            # Get Product detail
            #Product = models.Product.objects.get(product_num = product_num)
            # Create Purchase Form 
            #PurchaseForm = forms.Purchase(initial = {'product': Product})

        except Exception as e:
            print(e)
    # If request mehtof is POST
    elif request.method == 'POST':
        try:
            print("here")
            PurchaseForm = forms.Purchase(request.POST)
            if PurchaseForm.is_valid():
                PurchaseForm.save()
                Product = models.Product.objects.get(product_num = product_num)
                Product.amount += PurchaseForm.cleaned_data['amount']
                Product.setStock_Status()
                Product.save()
                return redirect('/admin')
        except Exception as e:
            print(e)
        

    return render(request, 'purchase_page.html', locals())


def sold_page(request, product_num = None):
    #print(product_num)
    try:
        print("session number test = "+str(request.session['sold_num']))
        soldnum = models.SoldNum.objects.get(num = request.session['sold_num'])
    except Exception as e:
        print(e)
        return redirect("/soldsystem/sold_num_list")
    try:
        Product = models.Product.objects.get(product_num = product_num)
    except Exception as e:
        print (e)
        # Create Purchase Form
    try:
        print("sold Number is "+request.session['sold_num'])
        soldnum = models.SoldNum.objects.get(num = request.session['sold_num'])
        total_prict = soldnum.get_total_cost()
        if Product:
            SoldForm = forms.Sold(initial = {'product': Product, 'sold_num': soldnum})
        else:
            SoldForm = forms.Sold(initial = {'sold_num': soldnum})
    except Exception as e:
        print (e)
    if request.method == 'GET':
        try: 
            pass
            # Get Product detail
            #Product = models.Product.objects.get(product_num = product_num)
            # Create Purchase Form 
            #SoldForm = forms.Purchase(initial = {'product': Product})

        except Exception as e:
            print(e)
    # If request mehtof is POST
    elif request.method == 'POST':  # save sold
        try:
            print("here")
            SoldForm = forms.Sold(request.POST)
            #SoldForm.files['producr'] = Product
            #SoldForm.fields['product']# = Product
            if SoldForm.is_valid():
                SoldForm.save()
                print(request.POST.get('product'))
                Product = models.Product.objects.get(id = request.POST.get('product'))
                #Product = models.Product.objects.get(product_num = product_num)
                Product.amount -= SoldForm.cleaned_data['amount']
                Product.setStock_Status()
                Product.save()
                return HttpResponseRedirect('/soldsystem/sold/list/')
        except Exception as e:
            print(e)
    return render(request, "sold_page.html", locals())

def show_sold_num_list(request):
    if request.method == 'GET':
        sold_num_list = models.SoldNum.objects.all()
        sold_num_form = forms.SoldNum()
    else:
        pass
        #redirect 404
    return render(request, "sold_num_list.html", locals())

def new_sold_num(request):
    print("new sold num"+ request.session['sold_num'])
    #del request.session['sold_num']
    if request.method == 'POST':
        sold_num = models.SoldNum()
        sold_num.set_num()
        sold_num.distribute = request.POST.get('distribute','')
        #print("----- request.POST.fields['distribute'] = ___" + request.POST.fields['distribute'])
        sold_num.save()
        request.session['sold_num'] = sold_num.num
    return redirect("/soldsystem/sold/list") # Sold list by Number
    #return render(request, "sold_cart.html", locals())

def show_sold_list(request):
    if request.method == 'GET':
        try:
            if not request.session['sold_num']:
                message = "Select a Sold Number"
            else:
                session_name = request.session['sold_num']
                sold_num = models.SoldNum.objects.get(num = request.session['sold_num'])
                sold_list = models.Sold.objects.filter(sold_num = sold_num)
            newsold = forms.Sold(initial = {'sold_num' : sold_num}) 
            return render(request, "sold_list.html", locals())
        except Exception as e:
            print(e)
            print("sold_list error")
            return redirect("/soldsystem/sold_num_list/")
    elif request.method == 'POST':
        return redirect("/soldsystem/sold/list/")


def sel_session(request):
    print("sold_num=======" + request.session['sold_num'])
    if request.method == 'POST':
        try:
            print(request.POST.get('selsession', ""))
            request.session['sold_num'] = request.POST.get('selsession', "")
            print("set session success")
        except Exception as e:
            print(e)
        
        return redirect("/soldsystem/sold/list")
