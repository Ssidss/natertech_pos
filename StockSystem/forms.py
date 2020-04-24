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

class Purchase(forms.ModelForm):
    class Meta:
        model = models.Purchase
        #widgets = {
        #    'purchase_date': DateInput(),
        #}
        fields = ['product', 'amount', 'price', 'reason', 'category',
        'memo', 'purchase_num']
    def __init__(self, *args, **kwargs):
        super(Purchase, self).__init__(*args, **kwargs)
        #self.fields['product'].widget.attrs['readonly'] = True
        #self.fields['volume'].label = 'volume'

class PurchaseNum(forms.ModelForm):
    class Meta:
        model = models.PurchaseNum
        fields = ['supplier']
    def __init__(self, *args, **kwargs):
        super(PurchaseNum, self).__init__(*args, **kwargs)

class Sold(forms.ModelForm):
    class Meta:
        model = models.Sold
        fields = ['product', 'amount', 'price', 'reason', 'fee', 'memo', 'sold_num']
        #widgets = {'id': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        super(Sold, self).__init__(*args, **kwargs)
        
class SoldNum(forms.ModelForm):
    class Meta:
        model = models.SoldNum
        fields = ['distribute']
        
    def __init__(self, *args, **kwargs):
        super(SoldNum, self).__init__(*args, **kwargs)
        self.fields['distribute'].label = 'Select Distribute'