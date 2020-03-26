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
    path('purchase/<slug:product_num>/', stock_views.purchase_page),
    #path('purchase/create/', views.purchase_create),
    path('sold/<slug:product_num>/', stock_views.sold_page),
    path('', stock_views.index_page),
    #path('product/<slug:p_num>/update/', views.ProductUpdate.as_view(), name = 'product_update'),
    re_path('^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT }),
    path('product_analysis/', ana_views.product_list_analysis),
    path('product_analysis/<slug:product_num>/', ana_views.product_analysis),
]
