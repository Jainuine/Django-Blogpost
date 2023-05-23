from django.shortcuts import render , redirect
from django.contrib.auth.models import User , auth
from django.contrib import messages
from django.http import HttpResponse
from .models import Post 
import json
import urllib.request


# Create your views here.
def index(request):
    posts = Post.objects.all()

    #the functionality has not been properly added
    '''res = urllib.request.urlopen('http://api.weatherstack.com/current?access_key=d2226ea4695d2649659abc4a31a09dfa&query=Pune').read()
    json_data = json.loads(res)
    datas = {
            "City": str(json_data['location']['name']),
            "Region": str(json_data['location']['region']),
            "temp": str(json_data['current']['temperature'])+' C',
            "timezone": str(json_data['location']['timezone_id']),
            "weather_icon": str(json_data['current']['weather_icons']),
            "weather": str(json_data['current']['weather_descriptions'])
        } 
          return render(request, 'index.html', { 'posts': posts , 'datas':datas})'''
    return render(request, 'index.html', { 'posts': posts })
  

def post(request, pk):
    posts = Post.objects.get(id=pk)
    return render(request, 'posts.html', {'posts': posts})

def register(request):
    if request.method == 'POST':
        username = request.POST['Username']
        email = request.POST['email']
        password = request.POST['Password']
        repassword = request.POST['Re Password']

        if password ==  repassword:
            
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Exists')
                return redirect('register')
            
            elif User.objects.filter(email=email).exists():
                messages.info(request , 'Email Already Used')
                return redirect('register')
            
        
            else: 
                user = User.objects.create_user(username = username, email = email, password = password )
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Password Not Same Re-Register')
            return redirect('register')

    else:
        return render(request,'register.html')
    


def login(request):
   if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user =  auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid')
            return redirect('login')

   return render(request,'login.html')

def weather(request):
    if request.method == 'POST':
        city = request.POST['city']
        res = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?units=metric&q='+city+'&appid=cb771e45ac79a4e8e2205c0ce66ff633').read()
        json_data = json.loads(res)
        data = {
            "country_code": str(json_data['sys']['country']),
            "coordinate": str(json_data['coord']['lon']) + ' ' +
            str(json_data['coord']['lat']),
            "temp": str(json_data['main']['temp'])+' C',
            "pressure": str(json_data['main']['pressure']),
            "humidity": str(json_data['main']['humidity']),
        }

    else:
        city = ''
        data = {}
    return render(request, 'weather.html', {'city': city, 'data': data})

