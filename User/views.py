from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
# Create your views here.
def index(request):
    return render(request,"index.html")

def contact(request):
    return render(request,"contact.html")

def about(request):
    return render(request,"about.html")

def error(request):
    return render(request,"404.html")

def team(request):
    return render(request,"team.html")

def register(request):
    if request.method=="POST":
        first=request.POST['fname']
        last=request.POST['lname']
        uname=request.POST['uname']
        email=request.POST['email']
        p1=request.POST['psw']
        p2=request.POST['psw1']
        if p1==p2:
            if User.objects.filter(username=uname).exists():
                messages.info(request,"Username Exists")
                return render(request,"register.html")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email Exists")
                return render(request,"register.html")
            else:
            
                #To store db
                user=User.objects.create_user(first_name=first,last_name=last,username=uname,email=email,
                 password=p1)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"Password Not Matching")
            return render(request,"register.html")
    else:
        return render(request,"register.html")
    return render(request,"register.html")

def login(request):
    if request.method=="POST":
        uname=request.POST['uname']
        p1=request.POST['psw']
        user=auth.authenticate(username=uname,password=p1)
        if user is not None:
            auth.login(request,user)
            return redirect ('data')
        else:
            messages.info(request,"Invalid Credentials")
            return render(request,"login.html")
    return render(request,"login.html")

def logout (request):
    auth.logout(request)
    return redirect('/')

def data(request):
    return render(request,"data.html")

def predict(request):
    if request.method=="POST":
        open=float(request.POST['open'])
        close=float(request.POST['close'])
        high=float(request.POST['high'])
        low=float(request.POST['low'])
        adj=float(request.POST['adj'])
        
        import pandas as pd
        df=pd.read_csv(r"static/TATAMOTORS.csv")
        print("**********")
        print(df.head())
        print("**********")
        print(df.shape)
        print("**********")
        print(df.isnull().sum())
        print("**********")
        print(df.dropna(inplace=True))
        df=df.drop("Date",axis=1)

        x1=df.drop("Volume",axis=1)
        y1=df["Volume"]
        
        from sklearn.model_selection import train_test_split
        x1_train,x1_test,y1_train,y1_test=train_test_split(x1,y1,test_size=0.3)
        import matplotlib.pyplot as plt 
        import seaborn as sns
        sns.heatmap(df.isnull())
        plt.show()
        
        plt.bar(df["Open"],df["Close"])
        plt.show()

        plt.barh(df["Close"],df["Low"])

        plt.show()
        plt.plot(x1_test,y1_test)
        plt.show()
        from sklearn.linear_model import LinearRegression
        reg=LinearRegression()
        reg.fit(x1_train,y1_train)
        pred_Stock=reg.predict(x1_test)

        plt.plot(x1_test,pred_Stock)
        plt.show()
        
        X_train=df[["Open","High","Low","Close","Adj Close"]]
        y_train=df["Volume"]

        from sklearn.linear_model import LinearRegression
        reg=LinearRegression()
        reg.fit(X_train,y_train)
        import numpy as np
        stock=np.array([[open,high,close,low,adj]],dtype=object)
        pred=reg.predict(stock)
        print("Predicted Stock Value: ",pred)
        return render(request,"predict.html",{"open":open,
        "close":close,"high":high,"low":low,"adj":adj,"stock":pred})
    return render(request,"predict.html")