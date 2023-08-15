from django import forms



class Form1(forms.Form):
    code = forms.CharField(max_length=100)