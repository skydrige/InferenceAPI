from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.models import User
from .inference.summary import Summarizer
from .Preprocessor import Preprocessor
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# from .models import *

# summarizer = Summarizer()


@csrf_protect
def index(request):
    processor = Preprocessor()
    content = processor.clean(request.POST['content'])
    print(content)
    if len(content) <= 10 or len(content) >= 20000:
        return JsonResponse({"summary": "Can't summarize this!"})
    text = summarizer.summarize(content)
    return JsonResponse({"summary": processor.formater(text)})


def test(request):
    text = summarizer.summarize(summarizer.text)
    return HttpResponse(Preprocessor().formater(text))


@csrf_protect
def direct_summary(request):
    processor = Preprocessor()
    content = processor.clean(request.POST['content'])
    if len(content) <= 10 or len(content) >= 20000:
        return render(request, 'contextForm.html', {'userInput': content, 'summary': "Can't summarize this!"})

    print("Direct: ", content)
    text = summarizer.summarize(content)
    return render(request, 'contextForm.html', {'userInput': content, 'summary': processor.formater(text)})


def direct_form(request):
    return render(request, 'contextForm.html')


@login_required(login_url='login')
def chat(request):
    return render(request, 'chat.html')


@csrf_protect
def signup(request):
    user = User()
    try:
        user.first_name = request.POST['name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.password = request.POST['password']
        user.save()
        return render(request, 'login.html', {'message': 'Account created!', 'user': user})
    except:
        return render(request, 'signup.html', {'error': 'Username already exists!', 'user': user})
    finally:
        return render(request, 'signup.html', {'user': user})


# def serve_login(request):
#     render(request, template_name='login.html')


@csrf_protect
def login_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except:
        return render(request, 'login.html')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(chat)
    else:
        return render(request, 'login.html', {'error': 'Invalid username or password!', 'details': user})


def logout_view(request):
    logout(request)
    render(request, 'login.html', {'message': 'You have been logged out!'})
