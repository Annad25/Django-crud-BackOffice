from django import forms

class AddProductForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    quantity = forms.IntegerField(label='Quantity')
    price = forms.DecimalField(label='Price')
