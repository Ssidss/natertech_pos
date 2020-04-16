from django.shortcuts import render
#import models
import StockSystem.models as smodels
import datetime

def product_list_analysis(request):
    re_dict = dict()
    sold = smodels.Sold.objects.all()
    sold_daily = []
    #today_sold = sold.filter(sold_date = datetime.date.today())
    #for i in range (30, -1, -1):
        #sold_daily.append(sold.filter(sold_date = datetime.date.today()-datetime.timedelta(days = i)))

    print(sold_daily)
    re_dict['sold_daily'] = enumerate(sold_daily)
    return render(request, "analysis_page.html", re_dict)

def product_analysis(request, product_num = None):
    if request.method == "GET":
        try:
            print(product_num)
            product_sold = smodels.Sold.objects.filter(product = smodels.Product.objects.get(product_num = product_num))
            # Dailys Sold 30 day
            sold_daily = []
            datearray = []
            for i in range(30, -1, -1):
                td = datetime.date.today()- datetime.timedelta(days = i)
                print(td)
                datearray.append("%s"%(td))
                sold_daily.append(product_sold.filter(sold_date = td))
                #sold_daily.append(product_sold.filter(sold_date = datetime.date.today()- datetime.timedelta(days = i)))
                #print(datetime.date.today()- datetime.timedelta(days = i))
            product_sold_amount = []
            product_disc_amount = []
            for i in sold_daily:
                if i:
                    sold_amount = 0
                    disc_amount = 0
                    for k in i:
                        if k.reason == 's':
                            sold_amount += 1
                        elif k.reason == 'd':
                            disc_amount += 1
                    print("sold" + str(sold_amount))
                    print("discount" + str(disc_amount))
                    product_sold_amount.append(sold_amount)
                    product_disc_amount.append(disc_amount)
                else:
                    product_sold_amount.append(0)
                    product_disc_amount.append(0)
        except Exception as e:
            print("error")
            print(e)
            #return 404
    return render(request, "analysis_page.html", locals())