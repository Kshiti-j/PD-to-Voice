from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('User_login/',views.User_login,name='User_login'), 
    path('logout/',views.logout,name='logout'), 
    path('PdfRead/', views.PdfRead, name='PdfRead'),
    path('Register/', views.Register, name='Register'),
    path('ListenPdf/', views.ListenPdf, name='ListenPdf'),
    path('test/', views.test, name='test'),
 
]

