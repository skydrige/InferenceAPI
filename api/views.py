from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_protect

from .Preprocessor import Preprocessor
from .inference.summary import Summarizer
from .models import test_session

summarizer = Summarizer()


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


@login_required(login_url='login_view')
def chat(request):
    name = request.user.first_name
    data = test_session.objects.filter(username=request.user)
    processor = Preprocessor()
    for i in data:
        i.model = processor.formater(i.model)
    return render(request, 'test.html', {'username': name, 'data': data})


@login_required(login_url='login_view')
@csrf_protect
def user_query(request):
    username = request.user.username
    query = request.POST.get('query')
    if len(query) < 10:
        return redirect(chat)
    previous = test_session.objects.filter(username=username).order_by('-timestamp')[:4]
    text = summarizer.reply(query, previous)
    conversation = test_session()
    message_id = test_session.objects.filter(username=username).order_by('-timestamp').first()
    if message_id is not None:
        conversation.message_id = username + "." + str(int(str(message_id).split(".")[-1]) + 1)
    else:
        conversation.message_id = username + '.' + '0'
    conversation.username = username
    conversation.user = query
    conversation.model = text
    conversation.timestamp = timezone.now()
    conversation.save()
    return redirect(chat)


@csrf_protect
def signup(request):
    user = User()
    try:
        user.first_name = request.POST['name']
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.set_password(request.POST['password'])
        user.save()
        return render(request, 'login.html', {'message': 'Account created!', 'user': user})
    except IntegrityError:
        return render(request, 'signup.html', {'error': 'User already existed!', 'user': user})
    except MultiValueDictKeyError:
        return render(request, 'signup.html')
    except Exception as e:
        return render(request, 'signup.html', {'error': e})


# def serve_login(request):
#     render(request, template_name='login.html')


@csrf_protect
def login_view(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except MultiValueDictKeyError:
        return render(request, 'login.html')
    except Exception as e:
        return render(request, 'login.html', {'error': e})
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(chat)
    else:
        return render(request, 'login.html', {'error': 'Invalid username or password!', 'details': user})


def logout_view(request):
    logout(request)
    return render(request, 'login.html', {'message': 'You have been logged out!'})


def test_html(request):
    return render(request, 'test.html')
