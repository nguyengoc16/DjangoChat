from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User

# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = 'Hi,,,,'
        return JsonResponse({'message':message,'response':response})
    return render(request,'chatbot.html')


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password= password)
        if user is not None:
            auth.login(request,user)
            return redirect('chatbot')
        else:
            error_message='Invalid username or password'
            render(request, 'register.html',{'error_message':error_message})
    return render(request, 'login.html')


def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user = User.objects.create_user(username=username, email= email, password=password1)
                user.save()
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = "error in creating account"
                return render(request,'register.html',{'error_message': error_message})
        else:
            error_message = 'Pass dont match'
            return render(request,'register.html',{'error_message': error_message})

    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')