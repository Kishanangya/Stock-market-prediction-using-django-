from django.urls import path
from .import views

urlpatterns=[
    path('',views.index,name='indx'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('error',views.error,name='error'),
    path('team',views.team,name='team'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('data',views.data,name='data'),
    path('predict',views.predict,name='predict'),
]