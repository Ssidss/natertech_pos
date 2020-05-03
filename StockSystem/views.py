from django.shortcuts import render, redirect
from StockSystem import models, forms
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
import datetime 
from django.contrib.sessions.models import Session
from django.utils import timezone
import woocommerce


WCAPI = woocommerce.API(
    url = "https://gardening.natertek.com/",
    consumer_key = "ck_d53e1b22959acb4bc5d8dd7a0e9e5a4773cc4adb",
    consumer_secret = "cs_4d92a26e3ce3a5358ea8e814e05c2390a9569bac"
)

def set_product_wpid(request):
    try:
        f = open("./../product_id.csv", mode = 'r')
    except Exception as e:
        print (e)
        return redirect("/")
    id_name_pair = f.read().split('\n')
    #id_name_dict = dict()
    for i in id_name_pair:
        #id_name_dict[name] = id
        try:
            name, id = i.split(',')
            product = models.Product.objects.get(name = name)
            product.wp_id = id
            print(product.name)
            product.save()
        except Exception as e:
            #print(e)
            pass
    
    f.close()
    return HttpResponseRedirect("/")

# url = "/"
def index_page(request):
    return render(request, 'index.html', locals())

# url = "product"
def product_list(request):
    productsystem = True
    try:
        Product_all = models.Product.objects.all()
        print("all success")
    except Exception as e:
        print(e)
    return render(request, 'product_list.html', locals())

# url = "prouct/<slug:product_num>"
def product_view(request, p_num = None):
    productsystem = True
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
                Productcontext.save()
            print("post success")
        except:
            print("post fail")
    #return JsonResponse(locals())
    return render(request, 'product_detail.html', locals())

# url = "purchase/<slug:product_num>"
def purchase_page(request, product_num = None):
    purchasesystem = True
    try:
        product = models.Product.objects.get(product_num = product_num)
    except Exception as e:
        print (e)
        product = None
    try:
        print("purchase Number is "+request.session['purchase_num'])
        purchasenum = models.PurchaseNum.objects.get(num = request.session['purchase_num'])
        total_cost = purchasenum.get_total_cost
        if product:
            PurchaseForm = forms.Purchase(initial = {'price': product.estimated_price, 'product': product, 'purchase_num': purchasenum})
        else:
            PurchaseForm = forms.Purchase(initial = {'purchase_num': purchasenum})
    except Exception as e:
        print (e)
        return redirect("/purchasesystem/purchase_num/list")
    if request.method == 'GET':
        try: 
            pass
        except Exception as e:
            print(e)
    # If request mehtof is POST
    elif request.method == 'POST':  # save purchase
        # delete method
        if product_num == "edit":
            try:
                purchase = models.Purchase.objects.get(id = request.POST.get('purchase_id'))
                if purchase.checkout: # restore product amount if purchase had checked out
                    purchase.product.amount -= purchase.amount
                    if purchase.product.wp_id:
                        WCAPI.post("products/"+str(purchase.product.wp_id), {"stock_quantity": purchase.product.amount})
                        print("update wp product "+ purchase.product.name + " success")
                    purchase.product.save()
                    purchase.checkout = False
                    purchase.save()
                    print("save success")
                PurchaseForm = forms.Purchase(instance = purchase)
                return render(request, "purchase/purchase_page.html", locals())
            except Exception as e:
                print (e)
                print("edit get fail")

        elif product_num == 'delete':  # delete single purchase 
            try:
                purchase = models.Purchase.objects.get(id = request.POST.get('purchase_id'))#.delete()
                if purchase.checkout: ## restore product amount if purchase had checked out
                    purchase.product.amount += purchase.amount
                    if purchase.product.wp_id:
                        WCAPI.post("products/"+str(purchase.product.wp_id), {"stock_quantity": purchase.product.amount})
                        print("update wp product "+ purchase.product.name + " success")
                    purchase.product.save()
                purchase.delete()
                print("Delete Success")
            except Exception as e:
                print(e)
                print("delete fail")
            return redirect("/purchasesystem/purchase/list/")
        try:
            try:
                purchase = models.Purchase.objects.get(id = request.POST.get('purchase_id'))
            except Exception as e:
                print(e)
                purchase = None
            PurchaseForm = forms.Purchase(request.POST, instance = purchase)
            if PurchaseForm.is_valid():
                PurchaseForm.save()
                return HttpResponseRedirect('/purchasesystem/purchase/list/')
        except Exception as e:
            print(e)
    return render(request, "purchase/purchase_page.html", locals())
        
# url = "purchasesystem/purchase_num/list/"
def show_purchase_num_list(request):
    purchasesystem = True
    if request.method == 'GET':
        purchase_num_list = models.PurchaseNum.objects.all().order_by('-id')
        purchase_num_form = forms.PurchaseNum()
    else:
        pass
        #redirect 404
    return render(request, "purchase/purchase_num_list.html", locals())

#url = "purchasesystem/purchase_num/new/"
def new_purchase_num(request):
    if request.method == 'POST':
        purchase_num = models.PurchaseNum()
        purchase_num.set_num()
        purchase_num.supplier = models.Supplier.objects.get(id = (request.POST.get('supplier', '')))
        purchase_num.save()
        request.session['purchase_num'] = purchase_num.num
    return redirect("/purchasesystem/purchase/list") # Sold list by Number
    #return render(request, "sold_cart.html", locals())

#url = "purchasesystem/purchase_num/delete"
# Delete purchase number and restore product amount if purchase had checked out
def delete_purchase_num(request):  
    try:
        num_id = request.POST.get("num_id")
        purchase_num = models.PurchaseNum.objects.get(id = num_id)
        purchase_list = models.Purchase.objects.filter(purchase_num = num_id)
        for purchase in purchase_list:
            if purchase.checkout:
                purchase.product.amount -= purchase.amount
                if purchase.product.wp_id:
                        print(WCAPI.post("products/"+str(purchase.product.wp_id), {"stock_quantity": purchase.product.amount}))
                        print("update wp product "+ purchase.product.name + " success")
                #sold.product.update_at = timezone.now
                purchase.product.save()
            purchase.delete()
        purchase_num.delete()
    except Exception as e:
        print(e)
        
    return redirect("/purchasesystem/purchase_num/list")

#url = "purchasesystem/purchase/list/"
def show_purchase_list(request):
    purchasesystem = True
    selsystem = "purchasesystem"
    if request.method == 'GET':
        try:
            five_num_list = models.PurchaseNum.objects.filter().order_by('-id')[:5]

        except Exception as e:
            print(e)
        try:
            if not request.session['purchase_num']:
                message = "Select a Purchase Number"
            else:
                session_name = request.session['purchase_num']
                purchase_num = models.PurchaseNum.objects.get(num = request.session['purchase_num'])
                purchase_list = models.Purchase.objects.filter(purchase_num = purchase_num)
                if all(purchase.checkout for purchase in purchase_list) and purchase_num.total_cost:
                    total_cost = purchase_num.total_cost 
                else:
                    total_cost = purchase_num.get_total_cost()
            newpurchase = forms.Purchase(initial = {'purchase_num' : purchase_num}) 
            return render(request, "purchase/purchase_list.html", locals())
        except Exception as e:
            print(e)
            print("purchase_list error")
            return redirect("/purchasesystem/purchase_num/list/")
    elif request.method == 'POST':
        return redirect("/purchasesystem/purchase/list/")

#url = "purchasesystem/checkout/"
# Purchase checkout and modify purchase product amount
def purchase_checkout(request):
    if request.method == 'POST':
        try:
            sel_session = request.session['purchase_num']
            purchase_num = models.PurchaseNum.objects.get(num = sel_session)
            purchase_list = models.Purchase.objects.filter(purchase_num = purchase_num)
            purchase_num.checkout = True
            for purchase in purchase_list:
                if purchase.checkout == True:
                    print("sold True")
                    continue
                else: # modify product amount and set purchase being checkout
                    purchase.checkout = True
                    purchase.product.amount += purchase.amount
                    if purchase.product.wp_id:
                        WCAPI.post("products/"+str(purchase.product.wp_id), {"stock_quantity": purchase.product.amount})
                        print("update wp product "+ purchase.product.name + " success")
                    purchase.product.setStock_Status()
                    purchase.product.save()
                    purchase.save()
            purchase_num.total_cost = request.POST.get('total_cost')
            purchase_num.set_num()
            purchase_num.save()
            print("save success")
            del request.session
            #print("checkout success")
            
        except Exception as e:
            print(e)
        return redirect("/purchasesystem/purchase_num/list")  

#url = "purchase/selsession/"
def purchase_selsession(request):
    if request.method == 'POST':
        try:
            #print(request.POST.get('selsession', ""))
            request.session['purchase_num'] = request.POST.get('selsession', "")
            print("set session success")
        except Exception as e:
            print(e)
        
        return redirect("/purchasesystem/purchase/list")

# url = "sold/<slug:product_num>"
def sold_page(request, product_num = None):
    soldsystem = True
    try:
        product = models.Product.objects.get(product_num = product_num)
    except Exception as e:
        print (e)
        product = None
        #return redirect("/soldsystem/sold_num_list")
    try:
        print("sold Number is "+request.session['sold_num'])
        soldnum = models.SoldNum.objects.get(num = request.session['sold_num'])
        total_cost = soldnum.get_total_cost
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
        # edit method 
        # edit single sold and set uncheckout
        if product_num == 'edit':
            try:
                sold = models.Sold.objects.get(id = request.POST.get('sold_id'))#.delete()
                if sold.checkout:  # restore product amount if sold had checked out
                    sold.product.amount += sold.amount 
                    if sold.product.wp_id:
                        WCAPI.post("products/"+str(sold.product.wp_id), {"stock_quantity": sold.product.amount})
                        print("update wp product "+ sold.product.name + " success")
                    sold.product.save()
                    sold.checkout = False
                    sold.save()
                SoldForm = forms.Sold(instance = sold)  #update
                return render(request, "sold_page.html", locals())

            except Exception as e:
                print(e)
                    
        elif product_num == 'delete':
            print("delete sold")
            try:
                sold = models.Sold.objects.get(id = request.POST.get('sold_id'))#.delete()
                if sold.checkout:  # restore product amount if sold had checked out
                    sold.product.amount += sold.amount 
                    if sold.product.wp_id:
                        WCAPI.post("products/"+str(sold.product.wp_id), {"stock_quantity": sold.product.amount})
                        print("update wp product "+ sold.product.name + " success")
                    #sold.product.update_at = timezone.now
                    sold.product.save()
                sold.delete()
                print("Delete Success")
            except Exception as e:
                print(e)
                print("delete fail")
            return HttpResponseRedirect("/soldsystem/sold/list/")
        try:
            try:
                sold = models.Sold.objects.get(id = request.POST.get('sold_id'))
            except Exception as e:
                print(e)
                sold = None
            SoldForm = forms.Sold(request.POST, instance = sold)
            if SoldForm.is_valid():
                SoldForm.save()
                return HttpResponseRedirect('/soldsystem/sold/list/')
        except Exception as e:
            print(e)
    return render(request, "sold_page.html", locals())

# url = "soldsystem/sold_num/list/"
def show_sold_num_list(request):
    soldsystem = True
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
    #soldsystem = True
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
# Delete sold number and restore product amount if sold had checked out
def delete_sold_nun(request):
    #soldsystem = True
    try:
        num_id = request.POST.get("num_id")
        sold_num = models.SoldNum.objects.get(id = num_id)
        sold_list = models.Sold.objects.filter(sold_num = num_id)
        for sold in sold_list:
            if sold.checkout:  # restore product amount
                sold.product.amount += sold.amount
                if sold.product.wp_id:
                        WCAPI.post("products/"+str(sold.product.wp_id), {"stock_quantity": sold.product.amount})
                        print("update wp product "+ sold.product.name + " success")
                #sold.product.update_at = timezone.now
                sold.product.save()
            sold.delete()
        sold_num.delete()
    except Exception as e:
        print(e)
        
    return redirect("/soldsystem/sold_num/list")

# url = "soldsystem/sold/list" get by session
# checkout detail
def show_sold_list(request):
    soldsystem = True
    selsystem = "soldsystem"
    if request.method == 'GET':
        try:
            five_num_list = models.SoldNum.objects.filter().order_by('-id')[:5]
            #five_num_list = zip(five_num_list, five_num_list[10:])
        except Exception as e:
            print(e)
        try:
            if not request.session['sold_num']:
                message = "Select a Sold Number"
            else:
                session_name = request.session['sold_num']
                sold_num = models.SoldNum.objects.get(num = request.session['sold_num'])
                sold_list = models.Sold.objects.filter(sold_num = sold_num)
                if all(sold.checkout for sold in sold_list) and sold_num.total_cost:
                    total_cost = sold_num.total_cost 
                else:
                    total_cost = sold_num.get_total_cost()
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
    #soldsystem = True
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
                    # restore product amount if sold had checked out
                    sold.product.amount -= sold.amount
                    if sold.product.wp_id:
                        WCAPI.post("products/"+str(sold.product.wp_id), {"stock_quantity": sold.product.amount})
                        print("update wp product "+ sold.product.name + " success")
                    sold.product.setStock_Status()
                    #sold.product.update_at = timezone.now
                    sold.product.save()
                    #sold.updated_at = timezone.now
                    sold.save()
            sold_num.total_cost = request.POST.get('total_cost')
            sold_num.set_num()
            #sold_num.update_at = timezone.now
            sold_num.save()
            print("save success")
            del request.session
            #print("checkout success")
            
        except Exception as e:
            print(e)
        return redirect("/soldsystem/sold_num/list")  
    

# url = "soldsystem/selsession"
def sel_session(request):
    #soldsystem = True
    #print("sold_num=======" + request.session['sold_num'])
    if request.method == 'POST':
        try:
            #print(request.POST.get('selsession', ""))
            request.session['sold_num'] = request.POST.get('selsession', "")
            print("set session success")
        except Exception as e:
            print(e)
        
        return redirect("/soldsystem/sold/list")

# get wordpress order by WCAPI periodically and modify DB quantity of product 
def wordpress_product_modify(request):
    print("wordpress_product_modify called")
    return HttpResponse(status = 200)
