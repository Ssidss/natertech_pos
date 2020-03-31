from django.contrib import admin
from StockSystem import models
from django.utils.safestring import mark_safe

class Show_Supplier(admin.ModelAdmin):
    model = models.Supplier
    list_display = ('name','phone', 'address', 'email',)
    ordering = ('name', 'phone', )

class Show_Category(admin.ModelAdmin):
    model = models.Category
    list_display = ('name', )
    ordering = ('name', )

class Show_Family(admin.ModelAdmin):
    model = models.Family
    list_display = ('chinese_name', 'name',)
    ordering = ('name', )

class Show_Genus(admin.ModelAdmin):
    model = models.Genus
    list_display = ('chinese_name', 'name', 'family',)
    ordering = ('family', 'name', )

class Show_Product(admin.ModelAdmin):
    model = models.Product
    list_display = ('name', 'amount', 'image_data', 'plant_size', 'product_num', 'stock_status', )
    ordering = ('name', 'plant_size', 'product_num', 'family', 'genus', )
    readonly_fields = ('image_data',)

class Show_Sold(admin.ModelAdmin):
    model = models.Sold
    list_display = ('product', 'amount', 'price', 'reason', 'fee', )
    ordering = ('product', )

class Show_Purchase_num(admin.ModelAdmin):
    model = models.PurchaseNum   # Purchas_Num -> PurchaseNum
    list_display = ('num', 'get_total_cost')
    ordering = ('num', )

class Show_Purchase(admin.ModelAdmin):
    model = models.Purchase   
    list_display = ('product', 'amount', 'price', 'reason', )
    ordering = ('product', )

class Show_Sold_Num(admin.ModelAdmin):
    model = models.SoldNum   # Sold_Nun -> SoldNum
    list_display = ('num', 'get_total_cost')
    ordering = ('num', )

admin.site.register(models.Supplier, Show_Supplier)
admin.site.register(models.Category, Show_Category)
admin.site.register(models.Family, Show_Family)
admin.site.register(models.Genus, Show_Genus)
admin.site.register(models.Product, Show_Product)
admin.site.register(models.Sold, Show_Sold)
admin.site.register(models.Purchase, Show_Purchase)
admin.site.register(models.PurchaseNum, Show_Purchase_num)  # Purchas_Num -> PurchaseNum
admin.site.register(models.SoldNum, Show_Sold_Num) # Sold_Nun -> SoldNum