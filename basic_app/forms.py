from django import forms
from django.contrib.auth.models import User
from basic_app.models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic')
class tradeform1(forms.Form):
    nameandtrans=forms.CharField(label="Stock Symbol(CAPS)")
    number_of_stocks_traded=forms.IntegerField()
    #user_id=forms.IntegerField()
class buyform(forms.Form):
    Stock_Name=forms.CharField()
    #User_id=forms.IntegerField()
    No_Stocks_To_Buy=forms.IntegerField()
class search1(forms.Form):
    query=forms.CharField(label="Enter first few alphabets(in CAPS) to search by name")
class search2(forms.Form):
    query1=forms.DecimalField(label="Enter lower bound on price")
    query2=forms.DecimalField(label="Enter upper bound on price")
class sell_form(forms.Form):
    Stock_Name=forms.CharField()
    #User_id=forms.IntegerField()
