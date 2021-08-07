'''
from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
# Create your views here.
def index(request):
    
    url='http://api.openweathermap.org/data/2.5/weather?q={}&appid=a93c86f249d3a2e3b3e64886618bd1c2'
    if request.method == 'POST': 
        form = CityForm(request.POST) 
        form.save() 
    #cities = City.objects.all()
    form = CityForm()
    cities = City.objects.all()

    weather_data = []

    for city in cities:

        url='http://api.openweathermap.org/data/2.5/weather?q={}&appid=a93c86f249d3a2e3b3e64886618bd1c2'

        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data, 'form' : form}
    return render(request, 'weather/index.html', context)

'''    
from django.shortcuts import render,redirect,get_object_or_404,HttpResponseRedirect
import requests
from .models import City
from .forms import CityForm
from django.views.generic.edit import DeleteView 
#from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView


def index(request):
    url='http://api.openweathermap.org/data/2.5/weather?q={}&appid=a93c86f249d3a2e3b3e64886618bd1c2'
    #city="London"

    err_msg = ''
    message = ''
    message_class = ''

    #r=requests.get(url.format(city)).json()
    #print(r.text)
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city_count = City.objects.filter(name=new_city).count()
            
            if existing_city_count == 0:
                r = requests.get(url.format(new_city)).json()

                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = 'City does not exist in the world!'
            else:
                err_msg = 'City already exists in the database!'

        if err_msg:
            message = err_msg
            message_class = 'is-danger'
        else:
            message = 'City added successfully!'
            message_class = 'is-success'
            
        


    form=CityForm()

    cities= City.objects.all()
    weather_data=[]


    for city in cities :

        


        r=requests.get(url.format(city)).json()

        city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)

    #print(weather_data)    

    context={"weather_data":weather_data,"form":form,"message":message,"message_class":message_class}  

    return render(request, 'weather/index.html',context)

def delete(request, city_name):

    
    City.objects.get(name=city_name).delete()

    return redirect('/')

''' 
def deleteTask(request,pk):
	item=City.objects.get(id=pk)

	if request.method == 'POST':
		item.delete()
		return redirect('/')

	context={'item':item}
	return render(request,'weather/delete.html',context) 

'''
'''
def delete(request,pk):
    City.objects.filter(id=pk).delete()
    items=City.objects.all()
    context={
        'items':items
    }
    return render(request,'index.html',context)
'''    