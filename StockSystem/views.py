from django.shortcuts import render, redirect
from StockSystem import models, forms
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime 
from django.contrib.sessions.models import Session

# url = "/"
def index_page(request):
    return render(request, 'index.html', locals())

# url = "product"
def product_list(request):
    try:
        Product_all = models.Product.objects.all()
        print("all success")
    except Exception as e:
        print(e)
    return render(request, 'product_list.html', locals())

# url = "prouct/<slug:product_num>"
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

# url = "purchase/<slug:product_num>"
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

# url = "sold/<slug:product_num>"
def sold_page(request, product_num = None):
    try:
        product = models.Product.objects.get(product_num = product_num)
    except Exception as e:
        print (e)
        product = None
        #return redirect("/soldsystem/sold_num_list")
    try:
        print("sold Number is "+request.session['sold_num'])
        soldnum = models.SoldNum.objects.get(num = request.session['sold_num'])
        total_prict = soldnum.get_total_cost()
        if product:
            SoldForm = forms.Sold(initial = {'price': product.estimated_price, 'product': product, 'sold_num': soldnum})
        else:
            SoldForm = forms.Sold(initial = {'sold_num': soldnum})
    except Exception as e:
        print (e)
        return redirect("/soldsystem/sold_num/list")
    if request.method == 'GET':
        try: 
            pass
        except Exception as e:
            print(e)
    # If request mehtof is POST
    elif request.method == 'POST':  # save sold
        # delete method
        if product_num == 'delete':
            try:
                sold = models.Sold.objects.get(id = request.POST.get('sold_id'))#.delete()
                if sold.checkout:
                    sold.product.amount += sold.amount
                    sold.product.save()
                sold.delete()
                print("Delete Success")
            except Exception as e:
                print(e)
                print("delete fail")
            return redirect("/soldsystem/sold/list/")
        try:
            SoldForm = forms.Sold(request.POST)
            if SoldForm.is_valid():
                SoldForm.save()
                return HttpResponseRedirect('/soldsystem/sold/list/')
        except Exception as e:
            print(e)
    return render(request, "sold_page.html", locals())

# url = "soldsystem/sold_num/list/"
def show_sold_num_list(request):
    if request.method == 'GET':
        sold_num_list = models.SoldNum.objects.all().order_by('-id')
        sold_num_form = forms.SoldNum()
    else:
        pass
        #redirect 404
    return render(request, "sold_num_list.html", locals())

# url = "soldsystem/sold_num/new"
def new_sold_num(request):
    #print("new sold num"+ request.session['sold_num'])
    #del request.session['sold_num']
    if request.method == 'POST':
        sold_num = models.SoldNum()
        sold_num.set_num()
        sold_num.distribute = 'r'#request.POST.get('distribute','')
        #print("----- request.POST.fields['distribute'] = ___" + request.POST.fields['distribute'])
        sold_num.save()
        request.session['sold_num'] = sold_num.num
    return redirect("/soldsystem/sold/list") # Sold list by Number
    #return render(request, "sold_cart.html", locals())

# url = "soldsystem/sold_num/delete"
def delete_sold_nun(request):
    try:
        num_id = request.POST.get("num_id")
        sold_num = models.SoldNum.objects.get(id = num_id)
        sold_list = models.Sold.objects.filter(sold_num = num_id)
        for sold in sold_list:
            if sold.checkout:
                sold.product.amount += sold.amount
                sold.product.save()
            sold.delete()
        sold_num.delete()
    except Exception as e:
        print(e)
        
    return redirect("/soldsystem/sold_num/list")

# url = "soldsystem/sold/list" get by session
def show_sold_list(request):
    if request.method == 'GET':
        try:
            five_sold_num_list = models.SoldNum.objects.filter().order_by('-id')[:5]
        except Exception as e:
            print(e)
        try:
            if not request.session['sold_num']:
                message = "Select a Sold Number"
            else:
                session_name = request.session['sold_num']
                sold_num = models.SoldNum.objects.get(num = request.session['sold_num'])
                total_cost = sold_num.get_total_cost
                sold_list = models.Sold.objects.filter(sold_num = sold_num)
            newsold = forms.Sold(initial = {'sold_num' : sold_num}) 
            return render(request, "sold_list.html", locals())
        except Exception as e:
            print(e)
            print("sold_list error")
            return redirect("/soldsystem/sold_num/list/")
    elif request.method == 'POST':
        return redirect("/soldsystem/sold/list/")

# url = "soldsystem/checkout
def sold_checkout(request):
    if request.method == 'POST':
        try:
            sel_session = request.session['sold_num']
            sold_num = models.SoldNum.objects.get(num = sel_session)
            #print(sold_num.num)
            sold_list = models.Sold.objects.filter(sold_num = sold_num)
            sold_num.checkout = True
            for sold in sold_list:
                if sold.checkout == True:
                    print("sold True")
                    continue
                else:
                    sold.checkout = True
                    #product = models.Product.objects.get(sold.product)
                    sold.product.amount -= sold.amount
                    sold.product.setStock_Status()
                    sold.product.save()
                    sold.save()
            sold_num.set_num()
            sold_num.save()
            print("save success")
            del request.session
            #print("checkout success")
            
        except Exception as e:
            print(e)
        return redirect("/soldsystem/sold_num/list")  
    

# url = "selsession"
def sel_session(request):
    #print("sold_num=======" + request.session['sold_num'])
    if request.method == 'POST':
        try:
            #print(request.POST.get('selsession', ""))
            request.session['sold_num'] = request.POST.get('selsession', "")
            print("set session success")
        except Exception as e:
            print(e)
        
        return redirect("/soldsystem/sold/list")
