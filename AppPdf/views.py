from django.shortcuts import render,redirect
from django import template
from django.contrib.sessions.models import Session
import string
import datetime
from datetime import date
from django.http import HttpResponse
from AppPdf.models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from googletrans import Translator, LANGUAGES
import PyPDF2
import io
import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import gtts 
from gtts import gTTS
from os.path import basename
from googletrans import Translator
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def home(request):
    return render(request,'home.html',{})

def User_login(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        password = request.POST['password']
        
        if User_Details.objects.filter(Username=Username, Password=password).exists():
            user = User_Details.objects.all().filter(Username=Username, Password=password)
            request.session['User_id'] = str(user[0].id)
            request.session['type_id'] = 'User'
            request.session['username'] = Username
            request.session['login'] = 'Yes'
            return redirect('/')
            
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('/User_login/')
    else:
        return render(request, 'User_login.html', {})


def logout(request):
    Session.objects.all().delete()
    return redirect('/')

def PdfRead(request):
    if request.method == 'POST':
        try:
            pdf = request.FILES.get('FileName')
            name = str(pdf).replace('.pdf','').replace(' ','')
            if not pdf:
                raise ValueError("No PDF file uploaded")

            Lang = request.POST.get('Languages')
            if not Lang:
                raise ValueError("Language selection is missing")
            
            # Check if the selected language is supported by Google Translate
            if Lang not in LANGUAGES:
                raise ValueError("Selected language is not supported")

            pdfFileObj = pdf.read() 
            pdfReader = PyPDF2.PdfReader(io.BytesIO(pdfFileObj))
            NumPages = len(pdfReader.pages)
            content = ""
            for i in range(NumPages):
                text = pdfReader.pages[i]
                content += text.extract_text()

            qwerty = content.replace("\n", "").replace("  ", " ").replace(",", " ")
            print(qwerty)
            
            translator = Translator()
            translation = translator.translate(qwerty, dest=Lang)
            print(translation)  # Add this line for debugging
            
            if translation is None or translation.text is None:
                raise ValueError("Translation failed or returned empty")

            outtext = translation.text
            print(outtext)  # Add this line for debugging
            
            x = datetime.datetime.now()
            currdate = x.strftime("%d-%w-%Y-%I-%M-%S")

            obj = gTTS(text=outtext, slow=False, lang=Lang)
            audio_file_name = f"{name}{currdate}.mp3"
            filename = os.path.join(BASE_DIR, 'media', 'Audio', audio_file_name)
            obj.save(filename)

            register = Pdf_Details(PdfName=pdf, Filename=f'/media/Audio/{audio_file_name}', UserId=request.session.get('User_id'))
            register.save()
            
            messages.info(request, 'Conversion Complete.')
            return redirect('/PdfRead/')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            print(f"An error occurred: {str(e)}")
            return redirect('/PdfRead/')
    else:
        return render(request, 'PdfRead.html', {})


def Register(request):
    if request.method == 'POST':
        First_Name = request.POST['First_name']
        Last_Name = request.POST['Last_name']
        Username = request.POST['Username']
        Dob = request.POST['Dob']
        Gender = request.POST['Gender']
        Phone = request.POST['Phone']
        Email = request.POST['Email']
        Password = request.POST['Password']
        final_address = request.POST['Address']
        City = request.POST['City']
        State = request.POST['State']
        

        if User_Details.objects.filter(Username=Username).exists():
            messages.info(request,'Username taken')
            return redirect('/AddOfficer/')

        elif User_Details.objects.filter(Email=Email).exists():
            messages.info(request,'Email Id taken')
            return redirect('/AddOfficer/')

        else:  
            register = User_Details( First_Name=First_Name, Last_Name=Last_Name, Dob=Dob, Gender=Gender ,Phone= Phone,Email= Email,Username= Username,Password=Password,Address=final_address,City=City,State=State)
            register.save()
            messages.info(request,'User Register Successfully')
            return redirect('/Register/')
    else:
        return render(request, 'Register.html', {})





def ListenPdf(request):
    if request.method == 'POST':
        
        return redirect('/ListenPdf/')
    else:
        Pdf_Det = Pdf_Details.objects.all().filter(UserId=request.session['User_id'])
        return render(request, 'ListenPdf.html', {'Pdf_Det':Pdf_Det})


def test(request):
    if request.method == 'POST':
        return redirect('/test/')
    else:
        return render(request, 'PlayMusic.html', {})
