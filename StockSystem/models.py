#Stock System Model
from django.db import models
import datetime
from django.utils.html import format_html


STOCK_STATUS = (('n', "none"), ('l', "less then 5"), ('s', "sufficient"))
REASON = (('s', "sold"), ('d', "discount"), ('r', "return"), ('b', "broken"), ('p', 'pruchase'))
DISTRIBUTE = (('r', "retailer"), ('s', "shapee"))

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('category_name', max_length=200)
    parent = models.ForeignKey('self', blank=True, null=True , default = None,related_name='children', on_delete = models.CASCADE)
    def __str__(self):
        return self.name

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('supplier_name', max_length=200)
    phone = models.CharField('supplier_phone', max_length=200, blank=True, default=None, null = True)
    address = models.CharField('supplier_address', max_length=200, blank=True, default=None, null = True)
    email = models.EmailField('supplier_email', max_length=200, blank=True, default=None, null = True)
    categorys = models.ManyToManyField(Category, blank=True, default=None)
    def __str__(self):
        return self.name

class Family(models.Model):  #科
    id = models.AutoField(primary_key=True)
    name = models.CharField('family_name', max_length=200)
    chinese_name = models.CharField('family_chinese_name', max_length=200, blank = True, default = None, null = True)
    def __str__(self):
        return self.chinese_name

class Genus(models.Model):  #屬
    id = models.AutoField(primary_key=True)
    name = models.CharField('genus_name', max_length=200)
    chinese_name = models.CharField('genus_chinese_name', max_length=200, blank = True, default = None, null = True)
    family = models.ForeignKey(Family, on_delete = models.CASCADE, blank=True, default=None)
    def __str__(self):
        return self.chinese_name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('product_name', max_length=200)
    amount = models.IntegerField('product_amount', default=0)
    product_num = models.SlugField('product_num', max_length=200, unique=True, blank = True, null = True, default = None)
    stock_status = models.CharField('product_stock_status', max_length=1, choices = STOCK_STATUS, blank=True, default=None, null = True) #Enum
    memo = models.TextField('product_memo', blank=True, default=None, null = True)
    family = models.ForeignKey(Family, on_delete = models.CASCADE, blank=True, default=None, null = True)
    genus = models.ForeignKey(Genus, on_delete = models.CASCADE, blank=True, default=None, null = True)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, blank=True, default=None, null = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank=True, default=None, null = True)
    image = models.ImageField("product_image", blank=True, null = True, default = None)
    length = models.FloatField("product_length", blank = True, null = True, default = 0.0)
    width = models.FloatField("product_width", blank = True, null = True, default = 0.0)
    high = models.FloatField("product_high", blank = True, null = True, default = 0.0)
    estimated_price = models.FloatField("product_estimated_price", blank = True, null = True, default= 0.0)
    plant_size = models.PositiveIntegerField("product_plant_size", blank = True, null = True, default = 0)
    def setStock_Status(self):
        if self.amount <= 0:
            self.stock_status = 'n'
        elif 0 < self.amount <5:
            self.stock_status = 'l'
        elif self.amount >= 5:
            self.stock_status = 's'
    def __str__(self):
        return self.name
    def image_data(self):
        #print(self.product_image.url)
        if self.image and hasattr(self.image, 'url'):
            return format_html(
            '<img src="%s" width="100px"/>'%(
            self.image.url)
            )
    image_data.short_description = 'product_image'

class SoldNum(models.Model): # Sold_Nun -> SoldNum
    #import Sold from .
    id = models.AutoField(primary_key = True)
    num = models.CharField('sold_num', max_length=200)
    sold_date = models.DateField('sold_date', blank=True, default=datetime.date.today, null = True)
    #sold = models.ManyToManyField(Sold, blank=True, default=None, null = True)
    def __str__(self):
        return self.num
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.sold_order_items.all())

class Sold(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.PositiveIntegerField('sold_amount')
    #sold_date = models.DateField()
    price = models.DecimalField('sold_revenue', max_digits=10, decimal_places = 0, default = 0)
    distribute = models.CharField('sold_distribute', max_length=1,choices = DISTRIBUTE, blank = True, default = None, null = True)  #eunm
    reason = models.CharField('sold_reason', max_length=1,choices = REASON, blank = True, null = True, default = 's')   #enum
    memo = models.TextField('sold_memo', blank=True, default=None, null = True)
    product = models.ForeignKey(Product, related_name = 'sold_items', on_delete = models.CASCADE, blank=True, default=None, null = True)
    fee = models.IntegerField('sold_fee', blank = True, default = 0)
    # Sold_Nun -> SoldNum
    sold_num = models.ForeignKey(SoldNum, related_name = 'sold_order_items', on_delete = models.CASCADE, blank=True, default=None, null = True)
    def get_cost(self):
        return self.price * self.amount
    def __str__(self):
        if self.product:
            return self.product.name
        else:
            return "No product"

class PurchaseNum(models.Model):   # Purchas_Num -> PurchaseNum
    #import Purchas from .
    id = models.AutoField(primary_key = True)
    num = models.CharField('purchase_num', max_length=200)
    purchase_date = models.DateTimeField('purchase_date', blank=True, default=datetime.datetime.now, null = True)
    #purchase = models.ManyToManyField(Purchase, blank=True, default=None, null = True)
    def __str__(self):
        return self.num
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.purchase_items.all())

class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.PositiveIntegerField('pruchase_amount', blank = True, default = 0)
    #purchase_date = models.DateTimeField('purchase_date', blank=True, default=datetime.datetime.now, null = True)
    price = models.DecimalField('purchase_expenses', max_digits=10, decimal_places=0, default = 0)
    reason =  models.CharField('purchase_reason', max_length=1, choices = REASON, blank = True, null = True, default = 'p')    #enum
    # Purchas_Num -> PurchaseNum
    purchase_num = models.ForeignKey(PurchaseNum, related_name = 'purchase_items', on_delete = models.CASCADE, blank=True, default=None, null = True)
    memo = models.TextField('purchase_memo', blank=True, default=None, null = True)
    product = models.ForeignKey(Product, related_name = 'purchase_order_items', on_delete = models.CASCADE, blank=True, default=None, null = True)
    supplier = models.ForeignKey(Supplier, on_delete = models.CASCADE, blank=True, default=None, null = True)
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank=True, default=None, null = True)
    def get_cost(self):
        return self.price * self.amount
    def __str__(self):
        if self.product:
            return self.product.name
        else:
            return "No product"
    
