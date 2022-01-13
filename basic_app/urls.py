from django.conf.urls import url
from basic_app import views
from django.urls import path
# SET THE NAMESPACE!
app_name = 'basic_app'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns=[
    url(r'^register/$',views.register,name='register'),
    url(r'^user_login/$',views.user_login,name='user_login'),
    path('i1/',views.fn2,name="fn2"),
    path('stocks/',views.allstocks,name='allstocks'),
    path('visual/',views.price_visuals,name='price_visuals'),
    path('form1/',views.form1,name='form1'),
    path('buyform/',views.buy_form,name='buy_form'),
    path('moredetails/',views.more_details,name='more_details'),
    path('searchby/',views.search_by,name='search_by'),
    path('sellform/',views.sellform,name='sellform'),
    path('searchbyprice/',views.search_price,name='search_price')

]
