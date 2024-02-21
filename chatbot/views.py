from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.auth.models import User
from localmodel import Model
from langchain.chains import RetrievalQA

# Create your views here.
def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = load_qa(message)[0]
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

def get_ready():
    llm, prompt, memory = Model()
    return llm, prompt, memory

def load_qa(query):
    llm, prompt, memory = get_ready()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        # retriever=retriever,
        # return_source_documents=True,
        chain_type_kwargs={"prompt": prompt, "memory": memory},
        verbose = True)
    res = qa(query)
    return res["result"], res["source_documents"]
