from django.shortcuts import render
from basic_app.forms import UserForm,UserProfileInfoForm,tradeform1,buyform,search1,sell_form,search2
from basic_app.models import UserProfileInfo,stocks
from basic_app.tables import SimpleTable
import pandas as pd
from django_pandas.io import read_frame
from django.db import connection
# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from collections import namedtuple
from django.http import HttpResponse
def namedtuplefetchall(cursor):
    # Return all rows from a cursor as a namedtuple
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')
def fn2(request):

    return render(request,'basic_app/afterlogin1.html')
@login_required
def special(request):
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered = False

    if request.method == 'POST':


        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)


        if user_form.is_valid() and profile_form.is_valid():


            user = user_form.save()
            user.set_password(user.password)


            user.save()




            profile = profile_form.save(commit=False)


            profile.user = user

            if 'profile_pic' in request.FILES:
                print('found it')
                profile.profile_pic = request.FILES['profile_pic']


            profile.save()
            registered = True

        else:

            print(user_form.errors,profile_form.errors)

    else:

        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)


        if user:

            if user.is_active:

                login(request,user)

                cursor=connection.cursor()
                #cursor.execute("select * from basic_app_stocks inner join basic_app_userprofileinfo on basic_app_userprofileinfo.stock1_id=basic_app_stocks.symbol")

                cursor.execute("select * from (select username,stock1_id,shares_count  from auth_user inner join basic_app_userprofileinfo on basic_app_userprofileinfo.user_id=auth_user.id ) as usertable inner join basic_app_stocks on usertable.stock1_id=basic_app_stocks.symbol where usertable.username= %s",[user.username])
                r=cursor.fetchall()
                #return HttpResponse("Hello")
                cursor.execute("select user_id  from auth_user inner join basic_app_userprofileinfo on basic_app_userprofileinfo.user_id=auth_user.id where username= %s",[user.username])
                #r1=cursor.fetchall()
                results=namedtuplefetchall(cursor)
                pv=results[0].user_id
                request.session['pv'] =pv
                request.session['pv1']=pv
                request.session['pv2']=pv
                request.session['username']=user.username

                return render(request,'basic_app/afterlogin1.html',{'data1': r})#,#'data2':r1})
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'basic_app/login.html', {})

def allstocks(request):
    cursor=connection.cursor()
    cursor.execute("select * from basic_app_stocks")
    r=cursor.fetchall()
    cursor.execute("select * from basic_app_company")
    r1=cursor.fetchall()
    return render(request,'basic_app/stocksandcompanies.html',{'d1':r,'d2':r1})

def login_pageenter(request):
    return HttpResponse("Hi!!")

def mode_check(request):
    cursor=connection.cursor()
    cursor.execute("select * from basic_app_stocks")
    r=cursor.fetchall()
    print(r)
    return HttpResponse("check console for output")
def price_visuals(request):
    return render(request,'basic_app/viz.html',{})
def search_name(request):
    return render(request,'basic_app/')

def buy_form(request):
    form=buyform()
    if request.method == 'POST':
        form=buyform(request.POST)
        if form.is_valid():
            stockname=form.cleaned_data['Stock_Name']
            #userid=form.cleaned_data['User_id']
            stocks_count=form.cleaned_data['No_Stocks_To_Buy']
            cursor=connection.cursor()
            ui=request.session.get('pv')
            #print("LOTS OF SHIT:",ui,"more shit")
            cursor.execute("select \"Last\" from basic_app_stocks where symbol=%s",[stockname])
            results2=namedtuplefetchall(cursor)

            un=request.session.get("username")
            #cursor.execute("")
            cursor.execute("select stock1_id,shares_count,\"Last\" from (select username,stock1_id,shares_count  from auth_user inner join basic_app_userprofileinfo on basic_app_userprofileinfo.user_id=auth_user.id ) as usertable inner join basic_app_stocks on usertable.stock1_id=basic_app_stocks.symbol where usertable.username=%s",[un])
            results1=namedtuplefetchall(cursor)
            cursor.execute("update basic_app_stocks set no_of_trades_today=no_of_trades_today+%s where symbol=%s",[results1[0].shares_count,results1[0].stock1_id])
            cursor.execute("CALL buy(%s,%s,%s)",[stockname,ui,stocks_count])
            return HttpResponse("{} Stocks of {} sold at {} per share. \n {} will be credited to your account \n {} shares of {} bought at {} per share. {} is the total cost of these newly acquired shares".format(results1[0].shares_count,results1[0].stock1_id,results1[0].Last,results1[0].shares_count*results1[0].Last,stocks_count,stockname,results2[0].Last,results2[0].Last*stocks_count))
    return render(request,'basic_app/buy_form.html',{'data':form})



def form1(request):
    form=tradeform1()

    if request.method == 'POST':
        form=tradeform1(request.POST)
        if form.is_valid():
            stockname=form.cleaned_data['nameandtrans']
            num_trad=form.cleaned_data['number_of_stocks_traded']
            #ui=form.cleaned_data['user_id']
            ui=request.session.get('pv1')
            un=request.session.get("username")
            cursor=connection.cursor()
            cursor.execute("select \"Last\" from (select username,stock1_id,shares_count  from auth_user inner join basic_app_userprofileinfo on basic_app_userprofileinfo.user_id=auth_user.id ) as usertable inner join basic_app_stocks on usertable.stock1_id=basic_app_stocks.symbol where usertable.username=%s",[un])
            results1=namedtuplefetchall(cursor)
            qa1=results1[0].Last
            cursor.execute("CALL trade(%s,%s,%s)",[stockname,num_trad,ui])
            return HttpResponse("{} stocks of {} sold at {} per share.\n {} will be credited to your account".format(num_trad,stockname,qa1,qa1*num_trad))

    return render(request,'basic_app/tradeform.html',{'form':form})

def more_details(request):
    cursor=connection.cursor()
    cursor.execute("select getcompany_with_highestcap()")
    r1=cursor.fetchall()
    cursor.execute("select getstock_withhighestopeningprice()")
    r2=cursor.fetchall()
    cursor.execute("select getstockprice_company_highest_cap()")
    r3=cursor.fetchall()
    cursor.execute("select get_most_tradedstock()")
    r4=cursor.fetchall()
    cursor.execute("select symbol,percinc,industry from basic_app_stocks inner join basic_app_company on basic_app_stocks.symbol=basic_app_company.stocksymbol_id where percinc=(select max(percinc) from basic_app_stocks)")

    r5=cursor.fetchall()
    cursor.execute("select max(percinc),industry from basic_app_stocks inner join basic_app_company on basic_app_stocks.symbol=basic_app_company.stocksymbol_id group by industry")
    r6=cursor.fetchall()
    cursor.execute("select symbol,percinc from basic_app_stocks order by percinc desc")
    r7=cursor.fetchall()
    return render(request,'basic_app/moreedetails.html',{'d1':r1,'d2':r2,'d3':r3,'d4':r4,'d5':r5,'d6':r6,'d7':r7})

def search_by(request):
    form=search1()
    if request.method == 'POST':

        form=search1(request.POST)
        if form.is_valid():
            letter=form.cleaned_data['query']
            #cursor=connection.cursor()
            #cursor.execute("select * from basic_app_stocks  where Last> %s",[letter])
            #r=cursor.fetchall()
            q=stocks.objects.filter(symbol__startswith=letter)
            #products = list(q.values_list('symbol','prevclose','open','high','low','Last','no_of_trades_today'))
            #t_products = list(zip(*products))
            table = SimpleTable(q)
            return render(request,'basic_app/search.html',{'d1':table})
    else:
        return render(request,'basic_app/search0.html',{'form':form})
def sellform(request):
    form=sell_form()
    if request.method == 'POST':
        form=sell_form(request.POST)
        if form.is_valid():
            s=form.cleaned_data['Stock_Name']
            #u=form.cleaned_data['User_id']
            ui=request.session.get('pv2')
            un=request.session.get("username")
            cursor=connection.cursor()
            cursor.execute("select shares_count,\"Last\" from (select username,stock1_id,shares_count  from auth_user inner join basic_app_userprofileinfo on basic_app_userprofileinfo.user_id=auth_user.id ) as usertable inner join basic_app_stocks on usertable.stock1_id=basic_app_stocks.symbol where usertable.username=%s",[un])
            results1=namedtuplefetchall(cursor)

            cursor.execute("CALL sell(%s,%s)",[s,ui])

            print(un)


            qa1=results1[0].shares_count
            qa2=results1[0].Last
            print(qa1)
            print(qa2)
            print(results1)
            return HttpResponse("All shares of {} sold at {} per share. \n Total amount credited to your account is {}".format(s,qa2,qa1*qa2))
    return render(request,'basic_app/sellform.html',{'form':form})


def search_price(request):
    form=search2()
    if request.method == 'POST':
        form=search2(request.POST)
        if form.is_valid():
            q=form.cleaned_data['query1']
            q1=form.cleaned_data['query2']
            cursor=connection.cursor()
            cursor.execute("select * from basic_app_stocks inner join basic_app_company on basic_app_stocks.symbol=basic_app_company.stocksymbol_id where \"Last\" between %s and %s",[q,q1])
            a1=cursor.fetchall()
            return render(request,'basic_app/displayrange.html',{'d1':a1})

    return render(request,'basic_app/buyform2.html',{'form':form})
