"""natertech_pos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from StockSystem import views as stock_views
from analysis_system import views as ana_views
from django.conf.urls import url
from django.views.static import serve
from . import settings

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path('product/<slug:p_num>/', stock_views.product_view),
    path('product/', stock_views.product_list),
    # purchase 進貨
    path('purchase/<slug:product_num>/', stock_views.purchase_page),
    path('purchasesystem/purchase_num/list/', stock_views.show_purchase_num_list),
    path('purchasesystem/purchase_num/new/', stock_views.new_purchase_num),
    path('purchasesystem/purchase_num/delete/', stock_views.delete_purchase_num),
    path('purchasesystem/purchase/list/', stock_views.show_purchase_list),
    path('purchasesystem/checkout/', stock_views.purchase_checkout),
    path('purchasesystem/selsession/', stock_views.purchase_selsession),
    path('', stock_views.index_page),
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT }),
    path('product_analysis/', ana_views.product_list_analysis),
    path('product_analysis/<slug:product_num>/', ana_views.product_analysis),
    # solesystem 出貨
    path('sold/<slug:product_num>/', stock_views.sold_page),
    path('soldsystem/sold_num/list/', stock_views.show_sold_num_list),
    path('soldsystem/sold_num/new/', stock_views.new_sold_num),
    path('soldsystem/sold_num/delete/', stock_views.delete_sold_nun),
    path('soldsystem/sold/list/', stock_views.show_sold_list),
    path('soldsystem/checkout/', stock_views.sold_checkout),
    path('soldsystem/selsession/', stock_views.sel_session)
]
