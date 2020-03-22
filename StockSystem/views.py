from django.shortcuts import render, redirect
from StockSystem import models, forms
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime 

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
    try:
        Product = models.Product.objects.get(product_num = product_num)
            # Create Purchase Form 
        SoldForm = forms.Sold(initial = {'product': Product})
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
    elif request.method == 'POST':
        try:
            print("here")
            SoldForm = forms.Sold(request.POST)
            #SoldForm.files['producr'] = Product
            #SoldForm.fields['product']# = Product
            if SoldForm.is_valid():
                SoldForm.save()
                Product = models.Product.objects.get(product_num = product_num)
                Product.amount -= SoldForm.cleaned_data['amount']
                Product.setStock_Status()
                Product.save()
                return redirect('/admin')
        except Exception as e:
            print(e)
    return render(request, "sold_page.html", locals())