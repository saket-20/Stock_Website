from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInfo(models.Model):

    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    # Add any additional attributes you want
    portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option=”build_ext” --global-option=”--disable-jpeg”
    profile_pic = models.ImageField(upload_to='profile_pics',blank=True)
    stock1=models.ForeignKey('stocks',on_delete=models.CASCADE,null=True)
    shares_count=models.PositiveIntegerField(null=True)
    # stock2=models.ForeignKey('stocks',on_delete=models.CASCADE,null=True)
    # shares_count2=models.PositiveIntegerField(null=True)
    # stock3=models.ForeignKey('stocks',on_delete=models.CASCADE,null=True)
    # shares_count3=models.PositiveIntegerField(null=True)
    # stock4=models.ForeignKey('stocks',on_delete=models.CASCADE,null=True)
    # shares_count4=models.PositiveIntegerField(null=True)
    # stock5=models.ForeignKey('stocks',on_delete=models.CASCADE,null=True)
    # shares_count5=models.PositiveIntegerField(null=True)
    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username

class stocks(models.Model):
    symbol=models.CharField(max_length=50,primary_key=True)
    prevclose=models.DecimalField(max_digits=6,decimal_places=2)
    open=models.DecimalField(max_digits=6,decimal_places=2)
    high=models.DecimalField(max_digits=6,decimal_places=2)
    low=models.DecimalField(max_digits=6,decimal_places=2)
    Last=models.DecimalField(max_digits=6,decimal_places=2)
    no_of_trades_today=models.PositiveIntegerField(default=50,null=False)
    percinc=models.DecimalField(max_digits=4,decimal_places=2,default=1.00,null=False)
class company(models.Model):
    stocksymbol=models.ForeignKey('stocks',on_delete=models.CASCADE,null=True)
    name=models.CharField(max_length=50,primary_key=True)
    market_cap=models.DecimalField(max_digits=50,decimal_places=2)
    industry=models.CharField(max_length=50)
