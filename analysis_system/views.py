from django.shortcuts import render
#import models
import StockSystem.models as smodels
import datetime

def product_analysis(request):
    redict = dict()
    sold = smodels.Sold.objects.all()
    sold_daily = []
    #today_sold = sold.filter(sold_date = datetime.date.today())
    for i in range (30, -1, -1):
        sold_daily.append(len(sold.filter(sold_date = datetime.date.today()-datetime.timedelta(days = i))))

    print(sold_daily)
    redict['sold_daily'] = enumerate(sold_daily)
    return render(request, "analysis_page.html", redict)