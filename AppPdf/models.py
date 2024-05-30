from django.db import models

class User_Details(models.Model):
    First_Name = models.CharField(max_length=50)
    Last_Name = models.CharField(max_length=50)
    Dob = models.CharField(max_length=50,default=None)
    Gender = models.CharField(max_length=10)
    Phone = models.IntegerField(default=None)
    Email = models.EmailField()
    Username = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    Address = models.CharField(max_length=100)
    City = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
      
    class Meta:
        db_table = 'User_Details'


class Pdf_Details(models.Model):
    PdfName = models.CharField(max_length=500,default=None)
    Filename = models.CharField(max_length=1000,default=None)
    UserId = models.CharField(max_length=50,default=None)
      
    class Meta:
        db_table = 'Pdf_Details'