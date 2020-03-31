#_*_ encoding: utf-8 _*_
from django import forms
from StockSystem import models

class DateInput(forms.DateInput):
    input_type = 'date'

class DateTimeInput(forms.DateTimeInput):
    input_type = 'datetime'

class Product(forms.ModelForm):
    
    class Meta:
        model = models.Product
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'name'
        self.fields['amount'].label = 'amount'
        self.fields['product_num'].label = 'product_number'
        self.fields['stock_status'].label = 'stock_status'
        self.fields['family'].label = 'family'
        self.fields['genus'].label = 'genus'
        self.fields['supplier'].label = 'supplier'
        self.fields['category'].label = 'category'

class Purchase(forms.ModelForm):
    class Meta:
        model = models.Purchase
        #widgets = {
        #    'purchase_date': DateInput(),
        #}
        fields = ['amount', 'price', 'reason', 'supplier', 'category', 'memo']
    def __init__(self, *args, **kwargs):
        super(Purchase, self).__init__(*args, **kwargs)
        #self.fields['product'].widget.attrs['readonly'] = True
        #self.fields['volume'].label = 'volume'

class Sold(forms.ModelForm):
    class Meta:
        model = models.Sold
        #widgets = {
        #    'sold_date': DateInput(),
        #}
        fields = ['product', 'amount', 'price', 'distribute', 'reason', 'fee', 'memo']
    def __init__(self, *args, **kwargs):
        super(Sold, self).__init__(*args, **kwargs)
        #self.fields['volume'].label = 'volume'