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
    ordering = ('name', 'family', )

class Show_Product(admin.ModelAdmin):
    model = models.Product
    list_display = ('name', 'amount', 'image_data', 'product_num', 'stock_status', )
    ordering = ('name', 'product_num', 'family', 'genus', )
    readonly_fields = ('image_data',)

class Show_Sold(admin.ModelAdmin):
    model = models.Sold
    list_display = ('product', 'amount', 'revenue', 'reason', 'sold_date', 'fee', )
    ordering = ('sold_date', )

class Show_Purchase_num(admin.ModelAdmin):
    model = models.Purchase_Num
    list_display = ('num', )
    ordering = ('num', )

class Show_Purchase(admin.ModelAdmin):
    model = models.Purchase
    list_display = ('product', 'amount', 'expenses', 'reason', 'purchase_date', )
    ordering = ('purchase_date', )

admin.site.register(models.Supplier, Show_Supplier)
admin.site.register(models.Category, Show_Category)
admin.site.register(models.Family, Show_Family)
admin.site.register(models.Genus, Show_Genus)
admin.site.register(models.Product, Show_Product)
admin.site.register(models.Sold, Show_Sold)
admin.site.register(models.Purchase, Show_Purchase)
admin.site.register(models.Purchase_Num, Show_Purchase_num)