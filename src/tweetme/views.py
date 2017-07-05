from django.shortcuts import render
#retrieve
#get template home.html 
def home(request):
    return render(request,"home.html",{})